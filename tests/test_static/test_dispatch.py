"""TestDispatch tests the Dispatch class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import Dispatch

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class TestDispatch(TestCase):
  """TestDispatch tests the Dispatch class."""

  def setUp(self) -> None:
    """Set up the test case."""
