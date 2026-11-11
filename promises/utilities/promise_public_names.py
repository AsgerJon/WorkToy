"""
PromisePublicNames promises the names 'worktoy.utilities' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.utilities
import worktoy.utilities.combinatorics


class PromisePublicNames(TestCase):
  """
  Every helper of 'worktoy.utilities' imports from the package itself,
  and the three combinatorial helpers from its 'combinatorics'
  subpackage. The file a helper lives in may change; the import from
  the package does not. Source: '__all__' of both packages.
  """

  def test_utilities(self) -> None:
    names = (
      'argsCount', 'bipartiteMatching', 'unpack', 'sliceLen', 'maybe',
      'textFmt', 'QuickDesc', 'stringList', 'Directory', 'joinWords',
      'wordWrap', 'replaceFlex', 'typeCast', 'hasCastRule', 'ValidSlice',
      'ExceptionInfo', 'resolveMRO', 'combinatorics',
    )
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.utilities, name))

  def test_combinatorics(self) -> None:
    names = ('indexPermutations', 'Arrangement', 'Arrangements')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.utilities.combinatorics, name))
