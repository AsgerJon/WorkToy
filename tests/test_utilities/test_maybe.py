"""
TestMaybe tests 'maybe' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import maybe
from . import UtilitiesTest


class TestMaybe(UtilitiesTest):
  """
  'maybe' picks the first argument that is not 'None', which is how a
  keyword left at 'None' takes its fallback without a falsy value such
  as '0' or an empty string being mistaken for one. The tests pin that
  only 'None' is skipped, and that 'None' comes back when nothing else
  is there.
  """

  def test_first_not_none(self) -> None:
    self.assertEqual(maybe(None, None, 'fallback'), 'fallback')
    self.assertEqual(maybe('first', 'second'), 'first')

  def test_falsy_values_kept(self) -> None:
    for value in (0, '', False, [], (), 0.0):
      with self.subTest(value=value):
        self.assertIs(maybe(None, value, 'ignored'), value)

  def test_all_none(self) -> None:
    self.assertIsNone(maybe(None, None))
    self.assertIsNone(maybe(None))

  def test_no_arguments(self) -> None:
    self.assertIsNone(maybe())

  def test_later_arguments_not_reached(self) -> None:
    #  The first hit is returned at once, so what follows is never read.
    self.assertEqual(maybe(1, None, 2), 1)
