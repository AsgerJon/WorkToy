"""
CoreTest subclass 'tests.BaseTest' to provide a shared base class for the
test classes in the 'tests.test_core' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class CoreTest(BaseTest):
  """
  CoreTest subclass 'tests.BaseTest' to provide a shared base class for the
  test classes in the 'tests.test_core' package.
  """
  pass
