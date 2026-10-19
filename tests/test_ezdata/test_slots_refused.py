"""
TestSlotsRefused subclasses 'EZTest' and pins that an 'EZData' class
body binding '__slots__' is refused with 'ReservedAttributeError' at the
line. The binding used to become a field named '__slots__', the first
positional one, so 'Point(1.0, 2.0)' handed 1.0 to the tuple. The field
values of an EZData class live in the instance '__dict__', so the class
declares no '__slots__' of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import ReservedAttributeError

from . import EZTest


class TestSlotsRefused(EZTest):
  """
  TestSlotsRefused provides tests for the refusal of '__slots__' in the
  body of an 'EZData' class.
  """

  def test_empty_slots_refused(self) -> None:
    """'__slots__ = ()' raises 'ReservedAttributeError' naming the name
    and the class, and the message says where the values live."""
    with self.assertRaises(ReservedAttributeError) as context:
      class Point(EZData):  # noqa: F841
        x = EZField[float](0.0)
        y = EZField[float](0.0)
        __slots__ = ()
    exception = context.exception
    self.assertEqual(exception.attributeName, '__slots__')
    self.assertEqual(exception.space.getClassName(), 'Point')
    self.assertIn("'__slots__'", str(exception))
    self.assertIn("'__dict__'", str(exception))
    self.assertNotIn('kwOnly=True', str(exception))

  def test_named_slots_refused(self) -> None:
    """A '__slots__' naming the fields is refused the same."""
    with self.assertRaises(ReservedAttributeError):
      class Point(EZData):  # noqa: F841
        x = EZField[float](0.0)
        y = EZField[float](0.0)
        __slots__ = ('x', 'y')

  def test_without_slots_positional(self) -> None:
    """Without '__slots__' the same class takes its two fields
    positionally."""

    class Point(EZData):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    point = Point(1.0, 2.0)
    self.assertEqual(len(point), 2)
    self.assertEqual((point.x, point.y), (1.0, 2.0))
