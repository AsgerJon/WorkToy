"""
TestBaseTest tests the 'BaseTest' class of the 'worktoy.work_test' package.
"Who tests the testers?" - "This class does."
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBaseTest(BaseTest):
  """
  TestBaseTest tests the 'BaseTest' class of the 'worktoy.work_test' package.
  "Who tests the testers?" - "This class does."
  """

  def test_arg_report(self, ) -> None:
    args = 'never', 'gonna', ('give', 'you', 'up'), 69, 420
    for chars in 24, 48, 77:
      report = self.argReport(*args, chars=chars, newLine=os.linesep)
      self.assertIsInstance(report, str)
      for line in str.split(report, os.linesep):
        self.assertLessEqual(len(str.strip(line)), chars)
