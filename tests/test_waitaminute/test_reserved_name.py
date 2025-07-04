"""
TestReservedName tests the ReservedName exception from the
'worktoy.waitaminute' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestReservedName(TestCase):
  """
  TestReservedName tests the ReservedName exception from the
  'worktoy.waitaminute' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()
