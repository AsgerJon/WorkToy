"""WorkToy - Guards - NoneGuard
This guard requires the value to be not-None"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.core import Function
from worktoy.guards import AbstractGuard


class NoneGuard(AbstractGuard):
  """WorkToy - Guards - NoneGuard
  This guard requires the value to be not-None"""

  def validate(self, obj: Any, name: str) -> Any:
    if obj is not None:
      return obj
    from worktoy.waitaminute import UnexpectedStateError
    raise UnexpectedStateError(name)

  def explicitGetter(self, obj: Any, cls: type) -> Function:
    """Exposes the validate method."""
    return lambda instance, name: self.validate(instance, name)
