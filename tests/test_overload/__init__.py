"""
The 'tests.test_overload' package provides compound tests for the
overloading functionality. This means particular overload cases
implementing a 'real world' use case.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._week_num import WeekNum
from ._flag_roll import FlagRoll

from ._overload_test import OverloadTest
from ._num_load import NumLoad

__all__ = [
    'WeekNum',
    'FlagRoll',
    'OverloadTest',
    'NumLoad',
]
