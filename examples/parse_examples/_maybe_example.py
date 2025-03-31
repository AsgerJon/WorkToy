"""The 'maybeExample' function demonstrates how to use the 'maybe'
function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import maybe
from random import shuffle


def maybeExample() -> None:
  """The 'maybeExample' function demonstrates how to use the 'maybe'
  function."""

  fallbackPower = 2

  def applyPower(base: int, power: int = None) -> int:
    """This implementation tests if power is None, and if so replaces with
    the fallback power"""
    if power is None:
      power = fallbackPower
    return base ** power

  def applyPowerSugar(base: int, power: int = None) -> int:
    """This implementation uses the 'maybe' function to choose the
    fallback value when the power argument is 'None'. """
    return base ** maybe(power, fallbackPower)

  print(applyPower(3, ))  # 9
  print(applyPowerSugar(4, ))  # 16

  print(maybe(None, 0, 69))  # 0
