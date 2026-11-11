"""
PromiseDistributions promises 'GaussianLengths' and the partitions of
'StochasticVariable', from 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.lorem_ipsum import GaussianLengths, StochasticVariable
from worktoy.lorem_ipsum import Sentence, Paragraph
from worktoy.waitaminute import TypeException


class PromiseDistributions(TestCase):
  """
  'GaussianLengths(mean, var, minVal, maxVal)' is a distribution of
  whole numbers between the two bounds, both included, and keeps the
  four as attributes a project may retune, converted as a box converts;
  a mean outside the bounds or a negative variance raises 'ValueError'.
  Every 'StochasticVariable' draws one value with 'sampleInteger', cuts a
  total into values within the bounds adding up to it with
  'partition(total)', and with 'partitionSpaced(total, spacing)' into
  values adding up to it once each value is given 'spacing' more; a
  total no count of values can reach raises 'ValueError'. Each sentence
  holds a 'GaussianLengths' of its own as 'clauseDist', and each
  paragraph one as 'sentenceDist'. Source: the docstrings of
  'StochasticVariable', 'GaussianLengths', 'Sentence' and 'Paragraph'.
  """

  def test_statistics(self) -> None:
    lengths = GaussianLengths(40, 15, 12, 70)
    self.assertEqual(lengths.mean, 40.0)
    self.assertIs(type(lengths.mean), float)
    self.assertEqual((lengths.var, lengths.minVal, lengths.maxVal),
                     (15.0, 12, 70))
    self.assertIsInstance(lengths, StochasticVariable)
    with self.assertRaises(TypeException):
      lengths.mean = 'forty'

  def test_refusals(self) -> None:
    with self.assertRaises(ValueError):
      GaussianLengths(100, 15, 12, 70)
    with self.assertRaises(ValueError):
      GaussianLengths(40, -1, 12, 70)

  def test_draws(self) -> None:
    lengths = GaussianLengths(40, 15, 12, 70)
    for _ in range(50):
      self.assertTrue(12 <= lengths.sampleInteger() <= 70)

  def test_partitions(self) -> None:
    lengths = GaussianLengths(40, 15, 12, 70)
    for total in (12, 70, 100, 300, 1000):
      with self.subTest(total=total):
        parts = lengths.partition(total)
        self.assertEqual(sum(parts), total)
        for part in parts:
          self.assertTrue(12 <= part <= 70)
        spaced = lengths.partitionSpaced(total + 20, 2)
        self.assertEqual(sum(spaced) + 2 * len(spaced), total + 20)

  def test_held_by_generators(self) -> None:
    first, second = Sentence(60), Sentence(60)
    self.assertIsInstance(first.clauseDist, GaussianLengths)
    self.assertIsNot(first.clauseDist, second.clauseDist)
    self.assertIsInstance(Paragraph(100).sentenceDist, GaussianLengths)

  def test_unreachable(self) -> None:
    with self.assertRaises(ValueError):
      GaussianLengths(40, 15, 12, 70).partition(5)
