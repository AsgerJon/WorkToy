"""
TestDuplicateHook tests that the DuplicateHookError correctly raises when
a hook is added multiple times to a class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from .. import MCLSTest


class TestDuplicateHook(MCLSTest):
  """
  TestDuplicateHook tests that the DuplicateHookError correctly raises when
  a hook is added multiple times to a class.
  """

  def test_duplicate_hook(self) -> None:
    """
    Tests that the DuplicateHookError is raised when a hook is added
    multiple times to a class.
    """
