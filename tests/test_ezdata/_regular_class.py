"""
RegularClass is a dataclass without inheritance and with all slots defined
as class variables. It is used to test the EZData class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData

if TYPE_CHECKING:  # pragma: no cover
  pass


class RegularClass(EZData):
  """
  RegularClass is a dataclass without inheritance and with all slots defined
  as class variables. It is used to test the EZData class.
  """

  a = 0
  b = 10
  c = 20
