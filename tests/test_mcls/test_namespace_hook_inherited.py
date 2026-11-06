"""
TestNamespaceHookInherited tests the defaults and the inherited hooks
'NamespaceHook' from 'worktoy.mcls.space_hooks' settles as a class is
compiled.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import METACALL
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.mcls.space_hooks import NamespaceHook
from worktoy.waitaminute.meta import UnboundClassHook
from . import MclsTest, LoggedMeta


class TestNamespaceHookInherited(MclsTest):
  """
  Every class hook must hold a value, so 'AbstractMetaclass' can tell a
  defined hook from an undefined one with one comparison. The first
  worktoy class of a hierarchy receives 'METACALL' at every hook, a
  subclass inherits what its bases hold, and a hook a plain base holds
  is checked by the rule of the body. The tests pin each of these, the
  placeholder of a claimed hook, and a hook handed back to the
  metaclass.
  """

  def test_first_worktoy_class_receives_metacall(self) -> None:
    class A(metaclass=LoggedMeta):
      pass

    for name in NamespaceHook._getClassDunders():
      with self.subTest(name=name):
        self.assertIs(A.__dict__[name], METACALL)

  def test_first_worktoy_class_binding_a_hook(self) -> None:
    class A(metaclass=LoggedMeta):
      @classmethod
      def __class_call__(cls, *args) -> tuple:
        return 'called', args

    self.assertEqual(A(1), ('called', (1,)))
    self.assertIsInstance(A.__dict__['__class_call__'], classmethod)
    names = NamespaceHook._getClassDunders()
    for name in [n for n in names if n != '__class_call__']:
      with self.subTest(name=name):
        self.assertIs(A.__dict__[name], METACALL)

  def test_first_worktoy_class_claiming_a_hook(self) -> None:
    class A(metaclass=BaseMeta):
      @classmethod
      @overload()
      def __class_call__(cls) -> str:
        return 'called'

    self.assertEqual(A(), 'called')
    self.assertIsInstance(A.__dict__['__class_call__'], Dispatcher)
    names = NamespaceHook._getClassDunders()
    for name in [n for n in names if n != '__class_call__']:
      with self.subTest(name=name):
        self.assertIs(A.__dict__[name], METACALL)

  def test_subclass_inherits_without_copies(self) -> None:
    class A(BaseObject):
      pass

    for name in NamespaceHook._getClassDunders():
      with self.subTest(name=name):
        self.assertNotIn(name, A.__dict__)
        self.assertIs(getattr(A, name), METACALL)

  def test_subclass_inherits_defined_hook(self) -> None:
    class A(BaseObject):
      @classmethod
      def __class_len__(cls) -> int:
        return 2

    class B(A):
      pass

    self.assertNotIn('__class_len__', B.__dict__)
    self.assertEqual(len(B), 2)

  def test_plain_base_hook_checked(self) -> None:
    class Plain:
      def __class_len__(cls) -> None:
        """Unchecked by any namespace, held to the rule later."""

    with self.assertRaises(UnboundClassHook) as context:
      class A(Plain, BaseObject):
        pass

    exception = context.exception
    self.assertEqual(exception.className, 'A')
    self.assertEqual(exception.hookName, '__class_len__')
    self.assertEqual(exception.baseName, 'Plain')
    self.assertIn("'Plain'", str(exception))

  def test_plain_base_classmethod_hook_passes(self) -> None:
    class Plain:
      @classmethod
      def __class_len__(cls) -> int:
        return 9

    class A(Plain, BaseObject):
      pass

    self.assertNotIn('__class_len__', A.__dict__)
    self.assertEqual(len(A), 9)

  def test_claimed_hook_replaces_inherited(self) -> None:
    class Plain:
      def __class_len__(cls) -> None:
        """Replaced by the overloads of the body."""

    class A(Plain, BaseObject):
      @classmethod
      @overload()
      def __class_len__(cls) -> int:
        return 6

    self.assertIsInstance(A.__dict__['__class_len__'], Dispatcher)
    self.assertEqual(len(A), 6)

  def test_hook_handed_back_to_metaclass(self) -> None:
    class A(BaseObject):
      @classmethod
      def __class_len__(cls) -> int:
        return 2

    class B(A):
      __class_len__ = METACALL

    self.assertEqual(len(A), 2)
    with self.assertRaises(TypeError) as context:
      len(B)
    self.assertEqual(str(context.exception), "type object 'B' has no len()")

  def test_by_hand(self) -> None:
    class Plain:
      def __class_len__(cls) -> None:
        """No classmethod."""

      @classmethod
      def __class_iter__(cls) -> None:
        """A classmethod."""

    space = BaseObject.__namespace__
    hook = NamespaceHook().__get__(space, type(space))
    hook._validateInheritedHook(Plain, '__class_iter__')
    with self.assertRaises(UnboundClassHook) as context:
      hook._validateInheritedHook(Plain, '__class_len__')
    self.assertEqual(context.exception.className, 'BaseObject')
    self.assertEqual(context.exception.hookName, '__class_len__')
    self.assertEqual(context.exception.baseName, 'Plain')
    self.assertIn("inherits '__class_len__' from its base 'Plain'",
                  str(context.exception))
