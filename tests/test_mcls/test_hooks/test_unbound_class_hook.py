"""
TestUnboundClassHook pins the class-creation guard holding routed
'__class_*__' hook names to classmethods and nothing else. The metaclass
invokes these hooks as bound classmethods, so a definition missing the
'@classmethod' decorator would fail confusingly at call time, or, in
the case of '__class_call__', silently swallow the first constructor
argument as the class, and an '@overload' there would become a
'Dispatcher' that expects an instance the metaclass never passes. The
guard raises 'UnboundClassHook' at the class-body line instead. A
classmethod bound again under a second hook name, and the 'METACALL'
sentinel, pass.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import METACALL
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import UnboundClassHook
from .. import MCLSTest


class TestUnboundClassHook(MCLSTest):
  """
  TestUnboundClassHook provides tests for the guard rejecting plain
  functions bound to routed '__class_*__' hook names.
  """

  def test_plain_function_hook_raises(self) -> None:
    """
    Testing that a routed hook defined as a plain function raises
    'UnboundClassHook' naming the class and the hook.
    """
    with self.assertRaises(UnboundClassHook) as context:
      class Foo(BaseObject):
        def __class_str__(cls) -> str:
          return 'Foo'  # pragma: no cover
    e = context.exception
    self.assertEqual(e.className, 'Foo')
    self.assertEqual(e.hookName, '__class_str__')
    self.assertEqual(str(e), repr(e))

  def test_plain_class_call_raises(self) -> None:
    """
    Testing that '__class_call__' as a plain function raises rather
    than silently swallowing the first constructor argument as the
    class.
    """
    with self.assertRaises(UnboundClassHook):
      class Bar(BaseObject):
        def __class_call__(cls, *args, **kwargs) -> None:
          pass  # pragma: no cover

  def test_staticmethod_hook_raises(self) -> None:
    """
    Testing that a routed hook defined as a staticmethod raises, since
    a staticmethod receives no class binding either.
    """
    with self.assertRaises(UnboundClassHook):
      class Baz(BaseObject):
        @staticmethod
        def __class_len__() -> int:
          return 0  # pragma: no cover

  def test_overload_hook_raises(self) -> None:
    """
    Testing that an '@overload' at a routed hook name raises
    'UnboundClassHook' naming the hook.
    """
    with self.assertRaises(UnboundClassHook) as context:
      class Foo(BaseObject):
        @overload()
        def __class_len__(cls) -> int:
          return 3  # pragma: no cover
    self.assertEqual(context.exception.hookName, '__class_len__')

  def test_plain_value_hook_raises(self) -> None:
    """
    Testing that a plain value at a routed hook name raises
    'UnboundClassHook'.
    """
    with self.assertRaises(UnboundClassHook):
      class Foo(BaseObject):
        __class_len__ = 3

  def test_second_name_and_metacall_pass(self) -> None:
    """
    Testing that a classmethod bound again under a second hook name, and
    'METACALL' written out, both pass.
    """

    class Foo(BaseObject):
      __class_len__ = METACALL

      @classmethod
      def __class_str__(cls) -> str:
        return 'Foo!'

      __class_repr__ = __class_str__

    self.assertEqual(str(Foo), 'Foo!')
    self.assertEqual(repr(Foo), 'Foo!')
    with self.assertRaises(TypeError):
      len(Foo)

  def test_classmethod_hook_passes(self) -> None:
    """
    Testing that the documented '@classmethod' form passes the guard
    and routes with the class bound.
    """
    class Good(BaseObject):
      @classmethod
      def __class_len__(cls) -> int:
        return 3

    self.assertEqual(len(Good), 3)
