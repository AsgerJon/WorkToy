"""
TestSmoke guarantees that the suite collects at least one test. Pytest
exits with code 5 when it collects nothing, and the mutation runner
treats a baseline that collects nothing as unmeasurable, so an empty
suite cannot be swept at all. This file keeps the suite non-empty no
matter which package folders exist yet.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest


class TestSmoke(BaseTest):
  """One test that cannot fail, so the suite is never empty."""

  def test_suite_collects(self) -> None:
    self.assertTrue(True)
