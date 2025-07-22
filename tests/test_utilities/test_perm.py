"""
TestPerm tests the 'perm' function from the 'worktoy.utilities._perm' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle
from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities import perm

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class TestPerm(UtilitiesTest):
  """
  TestPerm tests the 'perm' function from the 'worktoy.utilities._perm'
  module.
  """

  def test_len(self) -> Self:
    """Tests the initialization of the TestPerm class."""
    tomDickHarry = ['Tom', 'Dick', 'Harry']
    self.assertEqual(len([*perm(*tomDickHarry, ), ]), 6)

    return self

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
