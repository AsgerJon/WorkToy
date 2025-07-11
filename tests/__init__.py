"""
The 'tests' package contains unit tests for the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._base_test import BaseTest
from ._wyd import WYD  # Custom exception for testing

___all__ = [
    'WYD',  # Custom exception for testing
    'BaseTest',  # Base class for tests
]
