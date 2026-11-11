"""
PromisePublicNames promises the names 'worktoy.desc' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.desc


class PromisePublicNames(TestCase):
  """
  'AttriBox', 'FastBox', 'FixBox', 'Field', 'Alias', 'SymbolicName' and
  'BaseDescriptor' import from 'worktoy.desc'. Source: '__all__' of the
  package.
  """

  def test_names(self) -> None:
    names = ('FastBox', 'BaseDescriptor', 'Alias', 'Field', 'AttriBox',
             'FixBox', 'SymbolicName')
    for name in names:
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.desc, name))
