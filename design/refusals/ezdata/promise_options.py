"""
RefusedOptions holds the refusals that belong with
'design.promises.ezdata.promise_options'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData
from worktoy.waitaminute.ezdata import KwargsOnlyException


class RefusedOptions(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'frozen=True', or 'immutable' or 'hashable', refuses every
  assignment and deletion with 'AttributeError'. A positional argument to a
  class declared 'kwOnly=True' raises 'KwargsOnlyException'. Source: the
  docstrings of 'EZData', 'EZMeta' and 'EZHook'.
  """

  def test_frozen(self) -> None:
    for keyword in ('frozen', 'immutable', 'hashable'):
      with self.subTest(keyword=keyword):
        Point = type('Point', (EZData,), {'x': 0.0}, **{keyword: True})
        point = Point(1)
        with self.assertRaises(Exception) as refused:
          point.x = 2
        self.assertIsInstance(refused.exception, AttributeError)
        with self.assertRaises(Exception) as refused:
          point.note = 'scratch'
        self.assertIsInstance(refused.exception, AttributeError)
        with self.assertRaises(Exception) as refused:
          del point.x
        self.assertIsInstance(refused.exception, AttributeError)

  def test_keyword_only(self) -> None:
    for keyword in ('kwOnly', 'keywordOnly', 'kw_only'):
      with self.subTest(keyword=keyword):
        Config = type('Config', (EZData,), {'port': 80}, **{keyword: True})
        with self.assertRaises(Exception) as refused:
          Config(8080)
        self.assertIsInstance(refused.exception, KwargsOnlyException)
