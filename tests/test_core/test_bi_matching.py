"""
The 'TestBipartiteMatching' class provides unit tests for the
'worktoy.core.bipartiteMatching' function, which implements a
bipartite matching algorithm.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import CoreTest
from worktoy.utilities import bipartiteMatching

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBipartiteMatchingList(CoreTest):
  """
  Unit tests for list-based bipartiteMatching.
  """

  def testSimpleSuccess(self) -> None:
    slots = [
        (1, 2),
        (2, 3),
    ]
    result = bipartiteMatching(slots)
    self.assertEqual(len(result), 2)
    self.assertEqual(len(set(result)), 2)
    self.assertIn(result[0], slots[0])
    self.assertIn(result[1], slots[1])

  def testExactMatch(self) -> None:
    slots = [
        (0,),
        (1,),
        (2,),
    ]
    result = bipartiteMatching(slots)
    self.assertEqual(result, [0, 1, 2])

  def testAmbiguousSuccess(self) -> None:
    slots = [
        (1, 2, 3),
        (1, 2, 3),
        (1, 2, 3),
    ]
    result = bipartiteMatching(slots)
    self.assertEqual(len(result), 3)
    self.assertEqual(len(set(result)), 3)
    for i, value in enumerate(result):
      self.assertIn(value, slots[i])

  def testFailure(self) -> None:
    slots = [
        (1, 2),
        (1, 2),
        (1, 2),
    ]
    with self.assertRaises(ValueError):
      bipartiteMatching(slots)
