"""KeeTest provides a common test class for the 'tests.test_keenum'
module."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from worktoy.work_test import BaseTest

from .examples import FlagsExample, SubclassExample
from .examples import FileAccess, KeyboardModifier
from .examples import RootRGB, MoreRGB, EvenMoreRGB, RGBNum, Month, WeekDay

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeeTest(BaseTest):
  """KeeTest provides a common test class for the 'tests.test_keenum'
  module. """

  def setUp(self, ) -> None:
    self.exampleFlags = [
      FlagsExample,
      FileAccess,
      KeyboardModifier,
      SubclassExample,
    ]
    self.exampleNums = [
      RootRGB, MoreRGB, EvenMoreRGB, RGBNum, Month, WeekDay
    ]
