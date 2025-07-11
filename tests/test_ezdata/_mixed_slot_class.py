"""
MixedSlotClass provides a class that mixes between regular slots and slots
set as type hints.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import baseValues

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

from worktoy.ezdata import EZData


class RegPart(EZData):
  """
  RegPart provides the regular slots for the MixedSlotClass.
  """

  a = baseValues[0]


class AnnotPart(EZData):
  """
  AnnotPart provides the annotated slots for the MixedSlotClass.
  """

  b: int


class MixedBase(RegPart, AnnotPart):
  """
  MixedBase provides a class that mixes between regular slots and slots
  set as type hints.
  """

  c = baseValues[2]
