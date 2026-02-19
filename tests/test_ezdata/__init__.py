"""
The 'tests.test_ezdata' package contains tests for the 'worktoy.ezdata'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._regular_class import RegularClass
from ._sub_class import Mid1, Mid2, Mid3, SubClass
from ._ez_test import EZTest

__all__ = [
    'RegularClass',
    'Mid1',
    'Mid2',
    'Mid3',
    'SubClass',
    'EZTest',
]
