"""
TestUnorderedComparison subclasses 'EZTest' from the 'tests.test_ezdata'
package and provides tests for the comparison behavior of non-ordered
'EZData' classes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class TestUnorderedComparison(EZTest):
  """
  TestUnorderedComparison provides tests for the comparison behavior
  of 'EZData' classes declared without the 'ordered' flag. Comparing
  two instances of such a class must raise the interpreter's standard
  TypeError for unsupported comparisons, exactly as if the class had
  never defined any ordering dunders, rather than failing on a
  non-callable attribute.
  """

  def test_less_than_raises_standard_type_error(self) -> None:
    """
    The '<' operator on two instances of a non-ordered 'EZData'
    class raises the interpreter's standard TypeError naming the
    operator and the class, and the message never mentions
    'NoneType'.
    """

    class Point(EZData):
      x = EZField[int](0)
      y = EZField[int](0)

    with self.assertRaises(TypeError) as context:
      _ = Point(1, 1) < Point(2, 2)
    info = str(context.exception)
    self.assertIn("'<' not supported between instances", info)
    self.assertIn("'Point'", info)
    self.assertNotIn('NoneType', info)

  def test_every_ordering_operator_raises_type_error(self) -> None:
    """
    Each of the four ordering operators on a non-ordered 'EZData'
    class raises TypeError with the interpreter's standard message
    fragment for that operator.
    """

    class Point(EZData):
      x = EZField[int](0)
      y = EZField[int](0)

    samples = (
      (lambda a, b: a < b, '<'),
      (lambda a, b: a <= b, '<='),
      (lambda a, b: a > b, '>'),
      (lambda a, b: a >= b, '>='),
    )
    for compare, symbol in samples:
      with self.assertRaises(TypeError) as context:
        _ = compare(Point(1, 1), Point(2, 2))
      info = str(context.exception)
      self.assertIn("'%s' not supported between instances" % symbol, info)
      self.assertNotIn('NoneType', info)

  def test_subclass_does_not_inherit_parent_ordering(self) -> None:
    """
    A non-ordered subclass of an ordered 'EZData' class shadows the
    parent's ordering dunders, so comparing two subclass instances
    raises the standard TypeError instead of silently reusing the
    parent's comparison.
    """

    class Sorted(EZData, ordered=True):
      value = EZField[int](0)

    class Unsorted(Sorted):
      pass

    self.assertLess(Sorted(1), Sorted(2))
    with self.assertRaises(TypeError) as context:
      _ = Unsorted(1) < Unsorted(2)
    info = str(context.exception)
    self.assertIn("'<' not supported between instances", info)
    self.assertNotIn('NoneType', info)
