"""
ExampleTest is a subclass of 'worktoy.work_test.BaseTest' and provides a
base for each test in the 'tests.test_examples' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ExampleTest(BaseTest):
  """
  ExampleTest is a subclass of 'worktoy.work_test.BaseTest' and provides a
  base for each test in the 'tests.test_examples' package.
  """
  pass
