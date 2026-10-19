"""
TestInheritedUnboundHook subclasses 'SpaceHookTest' and pins that a
routed '__class_*__' hook inherited from a plain base, one no worktoy
metaclass built, is held to the same rule as one bound in the class
body: a plain function or a staticmethod is refused with
'UnboundClassHook' naming the base, as the class is created. Such a hook
used to be inherited unchecked and failed at the first call with
"missing 1 required positional argument: 'cls'".
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseMeta, BaseObject
from worktoy.waitaminute.meta import UnboundClassHook

from . import SpaceHookTest


class PlainFunctionMixin:
  """PlainFunctionMixin binds a hook to a plain function."""

  def __class_len__(cls) -> int:
    return 1  # pragma: no cover


class StaticMixin:
  """StaticMixin binds a hook to a staticmethod."""

  @staticmethod
  def __class_iter__():
    return iter(())  # pragma: no cover


class GoodMixin:
  """GoodMixin binds a hook to a classmethod."""

  @classmethod
  def __class_len__(cls) -> int:
    return 7


class TestInheritedUnboundHook(SpaceHookTest):
  """
  TestInheritedUnboundHook provides tests for routed hooks inherited from
  plain bases.
  """

  def test_plain_function_refused(self) -> None:
    """A plain function hook on a mixin is refused, naming the class,
    the hook and the base."""
    with self.assertRaises(UnboundClassHook) as context:
      class Foo(PlainFunctionMixin, BaseObject):
        pass
    e = context.exception
    self.assertEqual(e.className, 'Foo')
    self.assertEqual(e.hookName, '__class_len__')
    self.assertEqual(e.baseName, 'PlainFunctionMixin')
    self.assertIn("'PlainFunctionMixin'", str(e))
    self.assertEqual(str(e), repr(e))

  def test_staticmethod_refused(self) -> None:
    """A staticmethod hook on a mixin is refused as well, with a
    metaclass alone as much as with a worktoy base."""
    with self.assertRaises(UnboundClassHook):
      class Foo(StaticMixin, metaclass=BaseMeta):
        pass

  def test_classmethod_accepted(self) -> None:
    """A classmethod hook on a mixin is inherited and routed."""

    class Foo(GoodMixin, BaseObject):
      pass

    self.assertEqual(len(Foo), 7)

  def test_body_binding_unchanged(self) -> None:
    """A refusal of the class body's own binding names no base."""
    with self.assertRaises(UnboundClassHook) as context:
      class Foo(BaseObject):
        def __class_len__(cls) -> int:
          return 1  # pragma: no cover
    self.assertIsNone(context.exception.baseName)
