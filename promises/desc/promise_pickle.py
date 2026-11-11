"""
PromisePickle promises that an instance holding box values pickles,
from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle
from unittest import TestCase

from ._ticket import Ticket


class PromisePickle(TestCase):
  """
  An instance of a class defined at the top of a file pickles and
  unpickles with the values of its boxes, as instances of plain classes
  do. Source: the docstrings of 'AttriBox' and the 'desc' package.
  """

  def test_round_trip(self) -> None:
    ticket = Ticket()
    ticket.number = 12
    ticket.holder = 'Ada'
    restored = pickle.loads(pickle.dumps(ticket))
    self.assertIsNot(restored, ticket)
    self.assertEqual(restored.number, 12)
    self.assertEqual(restored.holder, 'Ada')
