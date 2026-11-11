"""
PromisePublicNames promises the names 'worktoy.ezdata' exports.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

import worktoy.ezdata


class PromisePublicNames(TestCase):
  """
  'EZData', 'EZField', 'fields', 'EZMeta', 'EZSpace', 'EZHook' and
  'EZStore' import from 'worktoy.ezdata'. Source: '__all__' and the
  docstring of the package.
  """

  def test_names(self) -> None:
    for name in ('EZData', 'EZField', 'fields', 'EZMeta', 'EZSpace',
                 'EZHook', 'EZStore'):
      with self.subTest(name=name):
        self.assertTrue(hasattr(worktoy.ezdata, name))
