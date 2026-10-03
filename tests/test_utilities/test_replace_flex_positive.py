"""
TestReplaceFlexPositive subclasses 'UtilitiesTest' and pins that
'replaceFlex' refuses an occurrence number below one with 'ValueError'.
The search loop ran no turn for it and spliced the replacement in before
the last character, so 'replaceFlex('abc', 'b', 'X', 0)' gave 'abXabc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import replaceFlex

from . import UtilitiesTest


class TestReplaceFlexPositive(UtilitiesTest):
  """
  TestReplaceFlexPositive provides tests for the occurrence number of
  'replaceFlex'.
  """

  def test_below_one_refused(self) -> None:
    """Zero and negative numbers raise 'ValueError'."""
    for n in (0, -1):
      with self.subTest(n=n):
        with self.assertRaises(ValueError):
          replaceFlex('abc', 'b', 'X', n)

  def test_positive(self) -> None:
    """A positive number replaces that occurrence, and the default the
    first."""
    self.assertEqual(replaceFlex('abab', 'b', 'X', 2), 'abaX')
    self.assertEqual(replaceFlex('abab', 'b', 'X'), 'aXab')
