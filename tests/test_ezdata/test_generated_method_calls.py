"""
TestGeneratedMethodCalls subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that the methods of an 'EZData' class are called as
Python calls any method. The generated 'asDict', 'asTuple' and 'replace'
take no positional arguments, so passing one raises 'TypeError' instead
of being dropped; 'replace(9)' in particular used to return an unchanged
copy. A method written in the class body takes keywords for its
positional parameters.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class TestGeneratedMethodCalls(EZTest):
  """
  TestGeneratedMethodCalls provides tests for calling the generated and
  the class-body methods of 'EZData' classes.
  """

  @staticmethod
  def _buildPoint() -> type:
    """The '_buildPoint' method builds a fresh 'EZData' class with two
    'float' fields and a method written in the class body."""

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

      def scaled(self, factor: float) -> tuple:
        return self.x * factor, self.y * factor

    return Point

  def test_replace_refuses_positional(self) -> None:
    """A positional argument to 'replace' raises 'TypeError' rather than
    returning an unchanged copy."""
    point = self._buildPoint()(1.0, 2.0)
    with self.assertRaises(TypeError):
      point.replace(9.0)

  def test_as_dict_refuses_positional(self) -> None:
    """A positional argument to 'asDict' raises 'TypeError'."""
    point = self._buildPoint()(1.0, 2.0)
    with self.assertRaises(TypeError):
      point.asDict(1)

  def test_as_tuple_refuses_positional(self) -> None:
    """A positional argument to 'asTuple' raises 'TypeError'."""
    point = self._buildPoint()(1.0, 2.0)
    with self.assertRaises(TypeError):
      point.asTuple(1)

  def test_body_method_takes_keyword(self) -> None:
    """A method written in the class body receives its positional
    parameter by keyword."""
    point = self._buildPoint()(1.0, 2.0)
    self.assertEqual(point.scaled(factor=2.0), (2.0, 4.0))

  def test_body_method_refuses_extra_positional(self) -> None:
    """A method written in the class body raises 'TypeError' for a
    positional argument beyond those it declares."""
    point = self._buildPoint()(1.0, 2.0)
    with self.assertRaises(TypeError):
      point.scaled(2.0, 3.0)

  def test_generated_methods_as_declared(self) -> None:
    """The generated methods called as declared still answer as
    before."""
    point = self._buildPoint()(1.0, 2.0)
    self.assertEqual(point.replace(x=9.0).asTuple(), (9.0, 2.0))
    self.assertEqual(point.asDict(), {'x': 1.0, 'y': 2.0})
    self.assertEqual(point.scaled(2.0), (2.0, 4.0))
