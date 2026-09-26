"""
TestTypeCastInstanceRule subclasses 'UtilitiesTest' and pins that
'typeCast' returns an instance of its target, or raises. For a target it
has no rule for, 'typeCast' calls the target on the value, and a target
whose constructor hands back something other than an instance of it is
refused with 'TypeCastException' instead of passing that on. The rule
asks for an instance, not for exactly the target, so a value already of
a subclass, or a constructor returning one, passes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestTypeCastInstanceRule(UtilitiesTest):
  """
  TestTypeCastInstanceRule provides tests for the rule that 'typeCast'
  returns an instance of its target.
  """

  def test_shifty_constructor_refused(self) -> None:
    """A target whose constructor returns something other than an
    instance of it raises 'TypeCastException', naming the target and the
    value given."""

    class Shifty:
      def __new__(cls, *args: Any) -> Any:
        return 42

    with self.assertRaises(TypeCastException) as context:
      typeCast(Shifty, 'x')
    e = context.exception
    self.assertIs(e.type_, Shifty)
    self.assertEqual(e.arg, 'x')

  def test_constructor_returning_subclass(self) -> None:
    """A target whose constructor returns an instance of a subclass
    passes, and that instance is returned."""

    class Shape:
      def __new__(cls, *args: Any) -> Any:
        return object.__new__(Square)

    class Square(Shape):
      pass

    self.assertIs(type(typeCast(Shape, 'x')), Square)

  def test_subclass_value_returned_unchanged(self) -> None:
    """A value already an instance of the target is returned as it is,
    a 'bool' for an 'int' target included."""
    self.assertIs(typeCast(int, True), True)

    class Parent:
      pass

    class Child(Parent):
      pass

    child = Child()
    self.assertIs(typeCast(Parent, child), child)
