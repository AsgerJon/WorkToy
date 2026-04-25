"""
TestPerm subclasses 'UtilitiesTest' and provides testing for the 'perm'
and 'permTraced' functions from the 'worktoy.utilities' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle
from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities import perm

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any, Iterator, TypeAlias, Union, Optional, Tuple


class TestPerm(UtilitiesTest):
  """
  TestPerm subclasses 'UtilitiesTest' and provides testing for the 'perm'
  and 'permTraced' functions from the 'worktoy.utilities' package.
  """

  @classmethod
  def factorial(cls, n: int) -> int:
    if n in [0, 1]:
      return 1
    return n * cls.factorial(n - 1)

  @classmethod
  def itemCounts(cls, *items) -> Iterator[tuple[Any, int]]:
    seen = []
    for item in items:
      if item not in seen:
        seen.append(item)
        yield (item, items.count(item))

  @classmethod
  def multinomialCoefficient(cls, *items) -> int:
    out = cls.factorial(len(items))
    for _, count in cls.itemCounts(*items):
      out //= cls.factorial(count)
    return out

  def test_len(self) -> None:
    """Tests the initialization of the TestPerm class."""
    tomDickHarry = ['Tom', 'Dick', 'Harry']
    permutations = perm(*tomDickHarry, )
    expectedCount = self.multinomialCoefficient(*tomDickHarry, )
    actualCount = len(permutations)
    self.assertEqual(expectedCount, actualCount)

  def test_52(self) -> None:
    """Testing playing cards"""
    cards = 'T', 'J', 'Q', 'K', 'A'
    self.assertEqual(len([*perm(*cards, )]), 120)

  def test_empty(self) -> None:
    """Testing empty """
    self.assertEqual(1, len([*perm(69, )]))
    self.assertEqual(1, len([*perm(), ]))

  def test_repeat(self, ) -> None:
    """Testing repeating permutations"""
    cards = 4 * ['clubs'] + 4 * ['hearts'] + ['diamond']
    perms = [*perm(*cards), ]
    for _ in range(1000):
      shuffle(cards)
      self.assertIn((*cards,), perms)
