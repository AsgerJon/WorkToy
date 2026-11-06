"""
Bag is a dataclass whose fields default to fresh containers.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField


class Bag(EZData):
  """
  A default is a recipe, not a cached object: 'EZField[list]()' builds
  a new list for every instance, so two bags share nothing.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  items = EZField[list]()
  labels = EZField[dict]()
  seeds = EZField[list]([1, 2])
