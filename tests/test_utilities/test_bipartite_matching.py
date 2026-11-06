"""
TestBipartiteMatching tests 'bipartiteMatching' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import bipartiteMatching
from worktoy.work_test.samplers import IntSampler
from . import UtilitiesTest


class TestBipartiteMatching(UtilitiesTest):
  """
  'bipartiteMatching' assigns a distinct index to every slot from the
  indices each slot allows, or refuses with 'ValueError' when no such
  assignment exists. The tests pin the docstring example, the two
  trivial inputs, the refusals, and that a first choice leading to a
  dead end is backed out of rather than reported as a failure.
  """

  def test_docstring_example(self) -> None:
    self.assertEqual(bipartiteMatching([(0, 1), (0,), (1, 2)]), [1, 0, 2])

  def test_no_slots(self) -> None:
    self.assertEqual(bipartiteMatching([]), [])

  def test_single_slot(self) -> None:
    self.assertEqual(bipartiteMatching([(7,)]), [7])

  def test_empty_slot_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      bipartiteMatching([(0, 1), ()])
    self.assertIn('distinct index', str(context.exception))

  def test_two_slots_one_index_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      bipartiteMatching([(0,), (0,)])
    self.assertIn('distinct index', str(context.exception))

  def test_backtracks_past_dead_end(self) -> None:
    #  All slots list two indices, so the first slot is expanded first
    #  and its first index leaves the other two slots one index between
    #  them. The second index is the one that works.
    self.assertEqual(bipartiteMatching([(0, 1), (0, 2), (0, 2)]), [1, 0, 2])

  def test_fewest_options_expanded_first(self) -> None:
    #  The last slot allows one index only, so it is settled first and
    #  the first slot is denied that index.
    self.assertEqual(bipartiteMatching([(2, 0), (0, 1), (2,)]), [0, 1, 2])

  def test_indices_compared_by_value(self) -> None:
    #  Indices beyond the small integers the interpreter caches are
    #  still told apart by value, not by identity.
    slots = [(int('1000000'), int('1000001')), (int('1000000'),)]
    self.assertEqual(bipartiteMatching(slots), [1000001, 1000000])

  def test_result_is_a_distinct_choice_per_slot(self) -> None:
    #  Each slot allows a distinct index of a shuffled range plus a few
    #  random extras, so a matching always exists.
    self.randomInteger = IntSampler(0, 5, seed=3, size=3)
    for _ in range(12):
      base = [*range(4)]
      self.randomInteger.random.shuffle(base)
      slots = [(base[i], *self.randomInteger.row) for i in range(4)]
      result = bipartiteMatching(slots)
      with self.subTest(slots=slots):
        self.assertEqual(len(result), 4)
        self.assertEqual(len(set(result)), 4)
        for value, options in zip(result, slots):
          self.assertIn(value, options)
