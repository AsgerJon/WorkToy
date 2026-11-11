"""
PromiseMaybe promises 'maybe' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import maybe


class PromiseMaybe(TestCase):
  """
  'maybe' gives the first of its arguments that is not 'None', so a
  keyword left at 'None' takes its fallback while a falsy value such as
  '0' is kept. With nothing but 'None', or nothing at all, it gives
  'None'. Source: the 'maybe' docstring and its examples.
  """

  def test_first_not_none(self) -> None:
    self.assertEqual(maybe(None, None, 'fallback'), 'fallback')

  def test_falsy_value_kept(self) -> None:
    self.assertEqual(maybe(0, 'ignored'), 0)
    self.assertEqual(maybe(None, '', 'ignored'), '')

  def test_nothing_found(self) -> None:
    self.assertIsNone(maybe(None, None))
    self.assertIsNone(maybe())
