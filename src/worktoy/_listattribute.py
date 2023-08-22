"""WorkToy - ListAttribute
Custom attribute implementing list instances."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import MutableAttribute


class ListAttribute(MutableAttribute):
  """WorkToy - ListAttribute
  Custom attribute implementing list instances."""

  def _typeCheck(self, value: object) -> bool:
    """Implementation tests if given value is a list"""
    return True if isinstance(value, list) else False

  def _typeGuard(self, value: list) -> list:
    """Ensures that the attribute does not somehow point at something
    other than a list."""
    if self._typeCheck(value):
      return value
    raise self.TypeException

  def __init__(self, *args, **kwargs) -> None:
    MutableAttribute.__init__(self, type_=list, defVal=[a for a in args])
