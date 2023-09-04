"""WorkToy - Guards - SomeGuard
Requires the object to be None."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.core import Function
from worktoy.guards import AbstractGuard


class SomeGuard(AbstractGuard):
  """WorkToy - Guards - SomeGuard
  Requires the object to be None."""

  def validate(self, obj: Any, name: str) -> Any:
    if obj is None:
      return obj
    from worktoy.waitaminute import ValueExistsError
    raise ValueExistsError(name, obj)

  def explicitGetter(self, obj: Any, cls: type) -> Function:
    """Exposes the validate method."""
    return lambda instance, name: self.validate(instance, name)
