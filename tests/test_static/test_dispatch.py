"""TestDispatch tests the Dispatch class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import StaticTest
from worktoy.static import Dispatch

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestDispatch(StaticTest):
  """TestDispatch tests the Dispatch class."""

  def test_ad_hoc(self) -> None:
    """
    Test ad-hoc metaclass functionality.
    """

    self.assertIsInstance(Dispatch, type)
