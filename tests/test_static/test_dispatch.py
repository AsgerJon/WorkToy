"""TestDispatch tests the Dispatch class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import Dispatch

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestDispatch(TestCase):
  """TestDispatch tests the Dispatch class."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_ad_hoc(self) -> None:
    """
    Test ad-hoc metaclass functionality.
    """

    self.assertIsInstance(Dispatch, type)
