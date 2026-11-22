"""
RefusedReplaceFlex holds the refusals that belong with
'design.promises.utilities.promise_replace_flex'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import replaceFlex


class RefusedReplaceFlex(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. An 'n' below one raises 'ValueError'. Source: the
  'replaceFlex' docstring and its examples.
  """

  def test_n_below_one_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      replaceFlex('foo', 'foo', 'X', 0)
    self.assertIsInstance(refused.exception, ValueError)

  def test_n_below_one_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      replaceFlex('foo', 'foo', 'X', -1)
    self.assertIsInstance(refused.exception, ValueError)
