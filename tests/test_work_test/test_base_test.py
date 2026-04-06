"""
TestBaseTest tests the 'BaseTest' class of the 'worktoy.work_test' package.
"Who tests the testers?" - "This class does."
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBaseTest(BaseTest):
  """
  TestBaseTest tests the 'BaseTest' class of the 'worktoy.work_test' package.
  "Who tests the testers?" - "This class does."
  """

  def test_dev_null(self, ) -> None:
    self.assertTrue(True)
