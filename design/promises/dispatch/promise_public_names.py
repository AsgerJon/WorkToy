"""
PromisePublicNames promises the names 'worktoy.dispatch' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.dispatch


class PromisePublicNames(TestCase):
  """
  'overload', 'Dispatcher', 'TypeSig', 'flexCall', 'isFlex',
  'CallMeMaybe', 'Permuter' and 'PermuterMethod' import from
  'worktoy.dispatch'. Source: '__all__' of the package.
  """

  def test_names(self) -> None:
    names = ('flexCall', 'isFlex', 'CallMeMaybe', 'Permuter',
             'PermuterMethod', 'TypeSig', 'Dispatcher', 'overload')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.dispatch, name))
