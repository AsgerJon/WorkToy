"""
TestRuntimeResolveType tests the 'runtimeResolveType' function from the
'worktoy.utilities' module. It verifies that the function correctly resolves
types by name.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import builtins
import sys
from unittest import TestCase

from worktoy.utilities import runtimeResolveType

from . import Foo

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Here:
  """Here is a class used by the TestRuntimeResolveType class to test
  runtimeResolveType.
  """
  pass


class TestRuntimeResolveType(TestCase):
  """TestRuntimeResolveType tests the 'runtimeResolveType' function from the
  'worktoy.utilities' module. It verifies that the function correctly
  resolves types by name.
  """

  def test_local_class(self) -> None:
    """Test that a local class can be resolved."""
    # self.assertEqual(runtimeResolveType('Here'), Here)

  def test_same_module(self, ) -> None:
    """Tests that a class define elsewhere in the same module can be
    resolved"""

  def test_ad_hoc(self) -> None:
    """Tests that a class defined ad-hoc can be resolved."""
