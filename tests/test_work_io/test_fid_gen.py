"""
TestFidGen tests the FidGen class and its functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import BaseTest

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any


class TestFidGen(BaseTest):
  """
  TestFidGen tests the FidGen class and its functionality.
  """

  def test_ad_hoc(self) -> None:
    """
    Test ad-hoc functionality of FidGen.
    """
    with self.assertRaises(Exception):
      raise Exception
