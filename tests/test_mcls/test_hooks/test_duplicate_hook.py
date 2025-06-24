"""
TestDuplicateHook tests that the DuplicateHookError correctly raises when
a hook is added multiple times to a class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.waitaminute import DuplicateHookError
from worktoy.mcls.hooks import AbstractHook

from tests import WYD

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestDuplicateHook(TestCase):
  """
  TestDuplicateHook tests that the DuplicateHookError correctly raises when
  a hook is added multiple times to a class.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_duplicate_hook(self) -> None:
    """
    Tests that the DuplicateHookError is raised when a hook is added
    multiple times to a class.
    """
