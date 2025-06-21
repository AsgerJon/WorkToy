"""DataField represents an entry in the EZData classes. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class DataField:
  """DataField represents an entry in the EZData classes. """
  __slots__ = ('key', 'type_', 'val')

  def __init__(self, key: str, type_: type, val: object) -> None:
    """Initialize the DataField object."""
    if not isinstance(key, str):
      raise TypeException('key', key, str)
    if not isinstance(type_, type):
      raise TypeException('type_', type_, type)
    if not isinstance(val, type_):
      raise TypeException('val', val, type_)
    self.key = key
    self.type_ = type_
    self.val = val

  def __str__(self) -> str:
    """Get the string representation of the DataField object."""
    infoSpec = """%s: %s = %s(%s)"""
    clsName = type(self).__name__
    typeName = self.type_.__name__
    return infoSpec % (self.key, typeName, clsName, self.val)

  def __repr__(self) -> str:
    """
    Get the code that would create this DataField object.
    """
    infoSpec = """%s(%r, %r, %r)"""
    return infoSpec % (type(self).__name__, self.key, self.type_, self.val)
