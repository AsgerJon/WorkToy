"""
PromiseStringList promises 'stringList' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import stringList
from worktoy.waitaminute import TypeException


class PromiseStringList(TestCase):
  """
  'stringList' splits strings on ', ', or on the 'separator' given,
  strips every piece and drops the empty ones, keeping the order. A
  list or tuple of separators splits by each in turn. A separator of
  any other type raises 'TypeException'. Source: the 'stringList'
  docstring and its examples.
  """

  def test_splits(self) -> None:
    self.assertEqual(stringList('a, b, c'), ['a', 'b', 'c'])
    self.assertEqual(stringList('a, b', 'c, d'), ['a', 'b', 'c', 'd'])

  def test_default_needs_the_space(self) -> None:
    self.assertEqual(stringList('a,b'), ['a,b'])
    self.assertEqual(stringList('a,b', separator=','), ['a', 'b'])

  def test_strips_and_drops_empty(self) -> None:
    self.assertEqual(stringList(' a ,  , b ', separator=','), ['a', 'b'])

  def test_several_separators(self) -> None:
    self.assertEqual(stringList('a;b,c', separator=[',', ';']),
                     ['a', 'b', 'c'])

  def test_bad_separator(self) -> None:
    with self.assertRaises(TypeException) as context:
      stringList('a, b', separator=7)
    e = context.exception
    self.assertEqual(e.varName, 'separator')
    self.assertEqual(e.actualObject, 7)
    self.assertIs(e.actualType, int)
    self.assertEqual(e.expectedTypes, (str, list, tuple))
