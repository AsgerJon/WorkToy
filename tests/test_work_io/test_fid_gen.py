"""
TestFidGen tests the FidGen class and its functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import BaseTest

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
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
