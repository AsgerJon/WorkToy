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

  def setUp(self) -> None:
    """Set up the test case."""
