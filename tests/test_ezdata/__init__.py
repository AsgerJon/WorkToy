"""
The 'tests.test_ezdata' package provides tests for the 'worktoy.ezdata'
package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from ._ez_test import EZTest
from . import examples

if sys.version_info >= (3, 10):
  from ._match_args_helpers import matchAsPoint2D
  from ._match_args_helpers import matchAsCircleKw
else:  # pragma: no cover
  from ._match_args_legacy_helpers import matchAsPoint2D
  from ._match_args_legacy_helpers import matchAsCircleKw

__all__ = (
  'EZTest',
  'examples',
  'matchAsPoint2D',
  'matchAsCircleKw',
)
