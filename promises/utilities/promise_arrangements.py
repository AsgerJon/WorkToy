"""
PromiseArrangements promises 'Arrangements' from
'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities.combinatorics import Arrangement, Arrangements


class PromiseArrangements(TestCase):
  """
  'Arrangements(*items)' holds every distinct ordering of 'items', each
  an 'Arrangement', so repeated items collapse: 'A', 'A', 'B' give three
  orderings, not six. Source: the 'Arrangements' docstring and its
  example.
  """

  def test_example(self) -> None:
    values = [a.values for a in Arrangements('A', 'A', 'B')]
    self.assertEqual(values, [('A', 'A', 'B'), ('A', 'B', 'A'),
                              ('B', 'A', 'A')])

  def test_every_ordering(self) -> None:
    arrangements = Arrangements('red', 'green', 'blue')
    self.assertEqual(arrangements.items, ('red', 'green', 'blue'))
    self.assertEqual(len(arrangements), 6)
    for arrangement in arrangements:
      self.assertIsInstance(arrangement, Arrangement)
    values = {a.values for a in arrangements}
    self.assertEqual(len(values), 6)
