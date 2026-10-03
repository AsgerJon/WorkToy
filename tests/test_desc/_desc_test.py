"""
DescTest provides a common base class for test classes in the
'tests.test_desc' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest


class DescTest(BaseTest):
  """
  DescTest provides a common base class for test classes in the
  'tests.test_desc' package.
  """

  @staticmethod
  def _unwrapSetName(
      exception: BaseException,
      expected: type,
  ) -> BaseException:
    """
    The exception a class body raised from '__set_name__', read back
    through the 'RuntimeError' that Python 3.7 through 3.11 wrap it in.
    From 3.12 onward it arrives unchanged.
    """
    if isinstance(exception, expected):
      return exception
    return exception.__cause__  # pragma: no cover (Python < 3.12)
