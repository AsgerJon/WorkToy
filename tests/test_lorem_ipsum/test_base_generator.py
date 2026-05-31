"""
TestBaseGenerator tests the 'BaseGenerator' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from worktoy.lorem_ipsum import BaseGenerator
from worktoy.lorem_ipsum import Clause
from worktoy.waitaminute import TypeException
from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBaseGenerator(LoremIpsumTest):
  """
  TestBaseGenerator provides tests for the 'BaseGenerator' class from the
  'worktoy.examples.lorem_ipsum' package.
  """

  def setUp(self) -> None:
    super().setUp()

  def test_init(self) -> None:
    """
    Testing that the 'BaseGenerator' initializes correctly.
    """
    for _ in range(16):
      count = randint(69, 420)
      generator = BaseGenerator(count)
      self.assertIsInstance(generator, BaseGenerator)
      self.assertEqual(generator.charCount, count)

    blank = BaseGenerator()
    self.assertIsInstance(blank, BaseGenerator)
    expectedCount = BaseGenerator.charCount.getPosArgs()[0]
    actualCount = blank.charCount
    self.assertEqual(expectedCount, actualCount)

  def test_non_numeric_char_count(self) -> None:
    """
    Testing that a non-numeric 'charCount' is rejected by the AttriBox type
    handling, while an integer assignment is stored.
    """
    clause = Clause(40)
    with self.assertRaises(TypeException):
      clause.charCount = 'not a number'
    clause.charCount = 50
    self.assertEqual(clause.charCount, 50)
