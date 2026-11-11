"""
PromiseClassHooks promises the class-level hooks of 'AbstractMetaclass'
from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import METACALL
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import UnboundClassHook


class PromiseClassHooks(TestCase):
  """
  A worktoy class defines how the class itself behaves, in its own body,
  through classmethods: '__class_iter__' and '__class_len__' for
  iteration and 'len', '__class_call__' for calling the class,
  '__class_instancecheck__' for 'isinstance', '__class_str__' for 'str',
  and the others 'AbstractMetaclass' lists. An operation without a hook
  behaves as for a plain class: 'len' and 'iter' raise 'TypeError',
  'bool' answers from '__class_len__' or else 'True', and 'in' searches
  what '__class_iter__' yields. A subclass sets an inherited hook to
  'METACALL' to hand the operation back, so 'METACALL' at
  '__class_call__' restores ordinary construction. A hook that is no
  classmethod raises 'UnboundClassHook'. '__class_init__' runs after the
  class is created, the declaring class included, with its name, bases,
  namespace and class keywords, which reach a plain base's
  '__init_subclass__' as well. The '__subclasshook__' of each direct
  base, its own or inherited, receives each new subclass and may refuse
  it by raising. Source: the 'AbstractMetaclass' docstring and the
  'METACALL' docstring.
  """

  def test_registry(self) -> None:
    class Planets(BaseObject):
      __names__ = ('Mercury', 'Venus')

      @classmethod
      def __class_iter__(cls):
        return iter(cls.__names__)

      @classmethod
      def __class_len__(cls) -> int:
        return len(cls.__names__)

      @classmethod
      def __class_call__(cls, index: int) -> str:
        return cls.__names__[index]

    self.assertEqual(list(Planets), ['Mercury', 'Venus'])
    self.assertEqual(len(Planets), 2)
    self.assertIn('Venus', Planets)
    self.assertEqual(Planets(1), 'Venus')

  def test_plain_defaults(self) -> None:
    class Plain(BaseObject):
      pass

    class Empty(BaseObject):
      @classmethod
      def __class_len__(cls) -> int:
        return 0

    with self.assertRaises(TypeError):
      len(Plain)
    with self.assertRaises(TypeError):
      iter(Plain)
    self.assertTrue(Plain)
    self.assertFalse(Empty)

  def test_instance_check_and_text(self) -> None:
    class Whole(BaseObject):
      @classmethod
      def __class_instancecheck__(cls, obj: object) -> bool:
        return isinstance(obj, int)

      @classmethod
      def __class_str__(cls) -> str:
        return 'whole numbers'

    class Plain(Whole):
      __class_instancecheck__ = METACALL

    self.assertIsInstance(3, Whole)
    self.assertEqual(str(Whole), 'whole numbers')
    self.assertNotIsInstance(3, Plain)

  def test_metacall_restores_construction(self) -> None:
    class Factory(BaseObject):
      @classmethod
      def __class_call__(cls, *args) -> str:
        return 'made'

    class Ordinary(Factory):
      __class_call__ = METACALL

    self.assertEqual(Factory(), 'made')
    self.assertIsInstance(Ordinary(), Ordinary)

  def test_unbound_hook(self) -> None:
    with self.assertRaises(UnboundClassHook) as context:
      class Counted(BaseObject):
        def __class_len__(cls) -> int:
          return 1
    e = context.exception
    self.assertIsInstance(e, SyntaxError)
    self.assertEqual(e.className, 'Counted')
    self.assertEqual(e.hookName, '__class_len__')

  def test_class_init(self) -> None:
    seen = []

    class Plugin(BaseObject):
      @classmethod
      def __class_init__(cls, name, bases, space, **kwargs) -> None:
        seen.append((cls.__name__, kwargs))

    class Mint(Plugin, flavor='mint'):
      pass

    self.assertEqual(seen, [('Plugin', {}), ('Mint', {'flavor': 'mint'})])

  def test_keyword_reaches_plain_base_too(self) -> None:
    class Flavored:
      def __init_subclass__(cls, flavor=None, **kwargs) -> None:
        cls.flavor = flavor
        super().__init_subclass__(**kwargs)

    class Plugin(BaseObject, Flavored):
      @classmethod
      def __class_init__(cls, name, bases, space, **kwargs) -> None:
        cls.keywords = kwargs

    class Mint(Plugin, flavor='mint'):
      pass

    self.assertEqual(Mint.flavor, 'mint')
    self.assertEqual(Mint.keywords, {'flavor': 'mint'})

  def test_subclass_hook(self) -> None:
    class Gate(BaseObject):
      @classmethod
      def __subclasshook__(cls, sub: type) -> None:
        if sub.__name__.startswith('Bad'):
          raise TypeError('refused')

    class GoodChild(Gate):
      pass

    with self.assertRaises(TypeError):
      class BadChild(Gate):
        pass
    self.assertTrue(issubclass(GoodChild, Gate))

  def test_subclass_hook_of_direct_bases(self) -> None:
    calls = []

    class Grand(BaseObject):
      @classmethod
      def __subclasshook__(cls, sub: type) -> None:
        calls.append((cls.__name__, sub.__name__))

    class Parent(Grand):
      pass

    class Kid(Parent):
      pass

    self.assertEqual(calls, [('Grand', 'Parent'), ('Parent', 'Kid')])
