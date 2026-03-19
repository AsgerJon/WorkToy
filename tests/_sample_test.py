"""
SampleTest subclasses 'BaseTest' and provides the base for teh test cases
in the 'worktoy.work_test.samples' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Callable, Never


class SampleTest(BaseTest):
  """
  SampleTest provides the base for the test cases in the
  'worktoy.work_test.samples' package.
  """
  pass
