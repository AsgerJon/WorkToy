"""
TestTypeCastInstanceRule subclasses 'UtilitiesTest' and pins that
'typeCast' returns an instance of its target, or raises. A class without
'__cast_as__' is refused whatever its constructor would do with the value,
and a '__cast_as__' handing back something other than an instance is
refused the same way. The rule asks for an instance, not for exactly the
target, so a value already of a subclass, or a hook returning one,
passes.
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
    """A target without '__cast_as__' raises 'TypeCastException' naming
    the target and the value, and its constructor is never asked."""

    class Shifty:
      def __new__(cls, *args: Any) -> Any:
        raise AssertionError('constructor called')  # pragma: no cover

    with self.assertRaises(TypeCastException) as context:
      typeCast(Shifty, 'x')
    e = context.exception
    self.assertIs(e.type_, Shifty)
    self.assertEqual(e.arg, 'x')

  def test_hook_returning_subclass(self) -> None:
    """A '__cast_as__' returning an instance of a subclass passes, and
    that instance is returned."""

    class Shape:
      @classmethod
      def __cast_as__(cls, value: Any) -> Any:
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
