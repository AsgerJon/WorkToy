"""
TestBipartiteMessage subclasses 'UtilitiesTest' and pins that
'bipartiteMatching' names no single slot when no assignment exists. It
named the slot the search tried first, which need not be at fault: in
'[(1, 2), (0,), (1, 2), (1, 2)]' it blamed slot 1, whose only candidate
is free, while the three other slots compete for two indices.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import bipartiteMatching

from . import UtilitiesTest


class TestBipartiteMessage(UtilitiesTest):
  """
  TestBipartiteMessage provides tests for the message of a failed
  matching.
  """

  def test_no_slot_blamed(self) -> None:
    """The message names none of the slots."""
    slots = [(1, 2), (0,), (1, 2), (1, 2)]
    with self.assertRaises(ValueError) as context:
      bipartiteMatching(slots)
    message = str(context.exception)
    for index in range(len(slots)):
      with self.subTest(index=index):
        self.assertNotIn('slot %d' % index, message)

  def test_same_message_for_empty_slot(self) -> None:
    """A slot without candidates fails the matching the same way."""
    with self.assertRaises(ValueError) as exhausted:
      bipartiteMatching([(1, 2), (0,), (1, 2), (1, 2)])
    with self.assertRaises(ValueError) as empty:
      bipartiteMatching([(0,), ()])
    self.assertEqual(str(exhausted.exception), str(empty.exception))
