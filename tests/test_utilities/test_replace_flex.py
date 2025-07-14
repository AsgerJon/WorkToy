"""
TestReplaceFlex tests the 'replaceFlex' function from the 'worktoy.utilities'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities import replaceFlex

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestReplaceFlex(UtilitiesTest):
  """
  TestReplaceFlex tests the 'replaceFlex' function from the
  'worktoy.utilities'
  package.
  """

  def test_basic(self) -> None:
    repeatingSubstring = """blabla%sderp"""
    base = ''.join([repeatingSubstring % 'lmao' for _ in range(69)])
    firstIndex = 6
    lastIndex = firstIndex + 4
    i = 0
    for i in range(69):
      res = replaceFlex(base, 'lmao', '????', i + 1)  # index from one
      if i:
        expected = 'lmao'
        actual = res[firstIndex:lastIndex]
        self.assertEqual(actual, expected)
        firstIndex += len(repeatingSubstring % expected)
        lastIndex = firstIndex + len(expected)
      expected = '????'
      actual = res[firstIndex:lastIndex]
      self.assertEqual(actual, expected)
    res = replaceFlex(base, 'breh', '????', i + 1)
    self.assertEqual(res, base)
