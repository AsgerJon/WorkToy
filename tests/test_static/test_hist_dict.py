"""
TestHistDict tests the HistDict class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import HistDict, ItemCall

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never


class TestHistDict(TestCase):
  """
  TestHistDict tests the HistDict class.
  """

  def setUp(self, ) -> None:
    """
    Set up the test case.
    """
    super().setUp()
