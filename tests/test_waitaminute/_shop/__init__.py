"""
The 'tests.test_waitaminute._shop' package stands in for a project
built upon worktoy that gives a warning of its own. A real project is a
top-level package, so this one registers itself as 'worktoy_shop' and
its warning class names that as its home: the warning then steps over
the files of this folder, as it would step over the files of the
project, and lands on the line that called 'ring'.

- ShopRisk
- ring
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from ._shop_risk import ShopRisk
from ._ring import ring

sys.modules['worktoy_shop'] = sys.modules[__name__]

__all__ = [
  'ShopRisk',
  'ring',
]
