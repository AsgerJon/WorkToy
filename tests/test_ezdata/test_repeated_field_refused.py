"""
TestRepeatedFieldRefused tests that an 'EZData' class refuses a field
given both by position and by keyword.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ezdata import RepeatedFieldException
from . import EZTest
from .examples import Point2D


class TestRepeatedFieldRefused(EZTest):
  """
  TestRepeatedFieldRefused tests positional and keyword arguments given
  together to the generated '__init__'. Each field may receive its value
  one way, and a field given both by position and by keyword raises
  'RepeatedFieldException' rather than letting one value replace the
  other.
  """

  def test_first_field_repeated(self) -> None:
    """
    Testing that a keyword repeating the first positional field is refused
    with 'RepeatedFieldException' naming the class and the field.
    """
    with self.assertRaises(RepeatedFieldException) as context:
      Point2D(1.0, x=2.0)
    exception = context.exception
    self.assertIs(exception.cls, Point2D)
    self.assertEqual(exception.fieldName, 'x')
    self.assertIn("'x'", str(exception))
    self.assertIn('Point2D', str(exception))

  def test_second_field_repeated(self) -> None:
    """
    Testing that a keyword repeating the second positional field is
    refused, naming that field.
    """
    with self.assertRaises(RepeatedFieldException) as context:
      Point2D(1.0, 2.0, y=3.0)
    self.assertEqual(context.exception.fieldName, 'y')

  def test_is_type_error(self) -> None:
    """
    Testing that 'RepeatedFieldException' is a 'TypeError', as Python's own
    refusal of multiple values for one argument is.
    """
    with self.assertRaises(TypeError):
      Point2D(1.0, x=2.0)

  def test_positional_then_other_keyword(self) -> None:
    """
    Testing that a keyword for a field no positional argument reached is
    accepted.
    """
    point = Point2D(1.0, y=2.0)
    self.assertEqual(point.asTuple(), (1.0, 2.0))
