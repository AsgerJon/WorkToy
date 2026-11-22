"""
RefusedGenerated holds the refusals that belong with
'design.promises.ezdata.promise_generated'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ezdata import ExtraPositionalException
from worktoy.waitaminute.ezdata import ExtraKeywordException
from worktoy.waitaminute.ezdata import RepeatedFieldException


class RefusedGenerated(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A value given to '__init__' that 'typeCast' does not convert
  to the type of its field is refused with 'TypeException'. Too many
  positional arguments raise 'ExtraPositionalException', an unknown keyword
  'ExtraKeywordException', and a field given by position and keyword
  'RepeatedFieldException', all 'TypeError's. Deleting a field raises
  'AttributeError'. Source: the docstrings of 'EZData', 'EZMeta' and
  'EZHook'.
  """

  def makePoint(self) -> type:
    class Point(EZData):
      x = 0.0
      y = 0.0

    return Point

  def test_init(self) -> None:
    Point = self.makePoint()
    with self.assertRaises(Exception) as refused:
      Point('one')
    self.assertIsInstance(refused.exception, TypeException)

  def test_init_refusals_1(self) -> None:
    Point = self.makePoint()
    with self.assertRaises(Exception) as refused:
      Point(1, 2, 3)
    self.assertIsInstance(refused.exception, ExtraPositionalException)

  def test_init_refusals_2(self) -> None:
    Point = self.makePoint()
    with self.assertRaises(Exception) as refused:
      Point(z=1)
    self.assertIsInstance(refused.exception, ExtraKeywordException)

  def test_init_refusals_3(self) -> None:
    Point = self.makePoint()
    with self.assertRaises(Exception) as refused:
      Point(1, x=2)
    self.assertIsInstance(refused.exception, RepeatedFieldException)

  def test_equality(self) -> None:
    Point = self.makePoint()
    with self.assertRaises(Exception) as refused:
      hash(Point(1, 2))
    self.assertIsInstance(refused.exception, TypeError)

  def test_assignment_and_deletion_1(self) -> None:
    Point = self.makePoint()
    point = Point()
    point.x = 5
    with self.assertRaises(Exception) as refused:
      point.x = 'five'
    self.assertIsInstance(refused.exception, TypeException)

  def test_assignment_and_deletion_2(self) -> None:
    Point = self.makePoint()
    point = Point()
    point.x = 5
    with self.assertRaises(Exception) as refused:
      del point.x
    self.assertIsInstance(refused.exception, AttributeError)
