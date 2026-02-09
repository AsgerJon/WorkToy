"""
The 'tests' package contains unit tests for the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._wyd import WYD
from ._base_test import BaseTest

___all__ = [
    'WYD',  # Custom exception for testing
    'BaseTest',  # Base class for tests
]

if __name__ == '__main__':  # pragma: no cover
  if WYD is BaseTest:
    infoSpec = """I can't believe PyCharm keeps yeeting BaseTest and WYD 
    whenever asked to optimize imports."""
    print(' '.join(infoSpec.split()))
