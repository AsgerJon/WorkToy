"""The overloader decorator applies the overloader flag on methods."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import CallMeMaybe, WorkDict


def overload(func: CallMeMaybe) -> CallMeMaybe:
  """Marks the decorated function for overloading"""
  WorkDict.applyOverload(func, )
  return func
