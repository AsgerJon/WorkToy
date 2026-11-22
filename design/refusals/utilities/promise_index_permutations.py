"""
RefusedIndexPermutations holds the refusals that belong with
'design.promises.utilities.promise_index_permutations'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities.combinatorics import indexPermutations


class RefusedIndexPermutations(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A negative 'n' raises 'ValueError' at the call, before
  anything is drawn. Source: the 'indexPermutations' docstring and its
  example.
  """

  def test_negative(self) -> None:
    with self.assertRaises(Exception) as refused:
      indexPermutations(-1)
    self.assertIsInstance(refused.exception, ValueError)
