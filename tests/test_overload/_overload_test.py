"""
OverloadTest provides a common base test case for all test classes in the
overload test module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator

  IntSample: TypeAlias = Iterator[tuple[int, ...]]


class OverloadTest(BaseTest):
  """
  OverloadTest provides a common base test case for all test classes in the
  overload test module.
  """
