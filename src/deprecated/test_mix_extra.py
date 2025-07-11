"""
TestMixExtra tests that mixing type-hinting slots and regular slots within
the same class body raises an error.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData

from typing import TYPE_CHECKING

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestMixExtra(EZTest):
  """
  TestMixExtra tests that mixing type-hinting slots and regular slots within
  the same class body raises an error.
  """

  def test_bad_mix(self) -> None:
    """Testing that mixing type-hinting slots and regular slots raises an
    error."""
