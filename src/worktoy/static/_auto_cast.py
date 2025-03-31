"""AutoCast subclasses AbstractCast and provides a general casting utility
for arbitrary types. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Any
except ImportError:
  Any = object

from worktoy.static import AbstractCast
from worktoy.text import typeMsg


class AutoCast(AbstractCast):
  """AutoCast subclasses AbstractCast and provides a general casting
  utility for arbitrary types. """

  __target_type__ = None

  def getTargetType(self, **kwargs) -> type:
    """Get the target type of the cast. Subclasses must implement this
    method to return the target type."""
    if self.__target_type__ is None:
      e = """Target type has not been set!"""
      raise RuntimeError(e)
    if isinstance(self.__target_type__, type):
      return self.__target_type__
    e = typeMsg('__target_type__', self.__target_type__, type)
    raise TypeError(e)

  def _setTargetType(self, targetType: type) -> None:
    """Set the target type of the cast. This method is used to set the
    target type of the cast."""
    if self.__target_type__ is not None:
      e = """Target type has already been set!"""
      raise RuntimeError(e)
    if not isinstance(targetType, type):
      e = typeMsg('targetType', targetType, type)
      raise TypeError(e)
    self.__target_type__ = targetType

  def _cast(self, *args, **kwargs) -> Any:
    """Cast the arguments to the target type."""
    cls = self.getTargetType()
    if len(args) == 1:
      if isinstance(args[0], cls):
        return args[0]
    return cls(*args, **kwargs)

  def __init__(self, targetType: type) -> None:
    """Initialize the AutoCast object."""
    self._setTargetType(targetType)
