"""KeeTest provides a common test class for the 'tests.test_keenum'
module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import BaseTest

from worktoy.keenum import Kee, KeeSpaceHook, KeeSpace, KeeMeta, KeeNum

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, Any, Callable


class KeeTest(BaseTest):
  """KeeTest provides a common test class for the 'tests.test_keenum'
  module. """
