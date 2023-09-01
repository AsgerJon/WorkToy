"""WorkToy - Guards - TypeGuard
Guards against wrong arguments on the basis of types."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.guards import AbstractGuard


class TypeGuard(AbstractGuard):
  """WorkToy - Guards - TypeGuard
  Guards against wrong arguments on the basis of types."""

  def __init__(self, type_: type, *args, **kwargs) -> None:
    AbstractGuard.__init__(self, type_, *args, **kwargs)
    self._expectedType = type_

  def validate(self, obj: Any, name: str) -> Any:
    """Validates based on types."""
    if isinstance(obj, self._expectedType):
      return obj
    from worktoy.waitaminute import TypeSupportError
    raise TypeSupportError(self._expectedType, obj, name)

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Subclasses must implement this method."""
    return lambda obj_, name='': self.validate(obj_, name)
