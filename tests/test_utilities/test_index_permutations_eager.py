"""
TestIndexPermutationsEager subclasses 'UtilitiesTest' and pins that
'indexPermutations' refuses a negative count as it is called. Being a
generator, it raised its 'ValueError' only at the first 'next'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities.combinatorics import indexPermutations

from . import UtilitiesTest


class TestIndexPermutationsEager(UtilitiesTest):
  """
  TestIndexPermutationsEager provides tests for when 'indexPermutations'
  checks its count.
  """

  def test_negative_refused_at_call(self) -> None:
    """The call itself raises, before anything is drawn from it."""
    with self.assertRaises(ValueError):
      indexPermutations(-1)

  def test_zero_positions(self) -> None:
    """No positions have one permutation, the empty one."""
    self.assertEqual([*indexPermutations(0)], [()])

  def test_permutations(self) -> None:
    """The permutations come in lexicographic order."""
    expected = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1),
                (2, 1, 0)]
    self.assertEqual([*indexPermutations(3)], expected)
