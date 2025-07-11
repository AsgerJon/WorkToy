"""
MultiBase provides a more complex inheritance structure with multiple
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import baseValues
from worktoy.ezdata import EZData

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class NEVER(EZData):  # upper-case to avoid confusion with typing.Never
  a = baseValues[0]


class GONNA(EZData):
  b = baseValues[1]


class GIVE(EZData):
  c = baseValues[2]


class YOU(EZData):
  d = baseValues[3 % 3]


class UP(EZData):
  e = baseValues[4 % 3]


class MultiBase(NEVER, ):
  """
  MultiBase provides a more complex inheritance structure with multiple
  base classes.
  """

  f = baseValues[5 % 3]
