"""
RefusedBipartiteMatching holds the refusals that belong with
'design.promises.utilities.promise_bipartite_matching'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import bipartiteMatching


class RefusedBipartiteMatching(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Slots that admit no such answer raise 'ValueError'. Source:
  the 'bipartiteMatching' docstring and its example.
  """

  def test_impossible(self) -> None:
    with self.assertRaises(Exception) as refused:
      bipartiteMatching([(0,), (0,)])
    self.assertIsInstance(refused.exception, ValueError)
