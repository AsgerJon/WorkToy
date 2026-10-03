"""
TestClassLenContains subclasses 'EZTest' and pins that 'len' and 'in'
work on an 'EZData' class, as iteration over its fields does: 'len' is
the number of fields and 'in' tests for one of them. 'EZMeta' defined
'__iter__' only, and the '__len__' and '__contains__' it inherited from
'AbstractMetaclass' consult the '__class_iter__' hook alone, so both
raised 'TypeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class Point(EZData):
  """Point has two fields."""

  x = EZField[int](0)
  y = EZField[int](0)


class Empty(EZData):
  """Empty has no fields."""


class TestClassLenContains(EZTest):
  """
  TestClassLenContains provides tests for 'len' and 'in' on an EZData
  class.
  """

  def test_len(self) -> None:
    """'len' is the number of fields, as iteration yields them."""
    self.assertEqual(len(Point), 2)
    self.assertEqual(len(Point), len([*Point]))
    self.assertEqual(len(Empty), 0)

  def test_contains(self) -> None:
    """'in' finds the fields of the class and nothing else."""
    for field in Point.fields:
      self.assertIn(field, Point)
    self.assertNotIn('x', Point)
    self.assertNotIn(Point.fields[0], Empty)
