"""
PromiseBipartiteMatching promises 'bipartiteMatching' from
'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import bipartiteMatching


class PromiseBipartiteMatching(TestCase):
  """
  'bipartiteMatching(slots)' gives one index per slot, in slot order,
  each taken from that slot's candidates and no two alike. Which of
  several valid answers comes back is not promised. Slots that admit no
  such answer raise 'ValueError'. Source: the 'bipartiteMatching'
  docstring and its example.
  """

  def test_example(self) -> None:
    self.assertEqual(bipartiteMatching([(0, 1), (0,), (1, 2)]), [1, 0, 2])

  def test_any_valid_answer(self) -> None:
    slots = [(0, 1, 2), (0, 1), (1, 2), (0, 1, 2, 3)]
    answer = bipartiteMatching(slots)
    self.assertEqual(len(answer), len(slots))
    self.assertEqual(len(set(answer)), len(answer))
    for index, options in zip(answer, slots):
      self.assertIn(index, options)

  def test_no_slots(self) -> None:
    self.assertEqual(bipartiteMatching([]), [])

  def test_impossible(self) -> None:
    with self.assertRaises(ValueError):
      bipartiteMatching([(0,), (0,)])
