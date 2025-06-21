"""
'AliasException' is raised when an 'Alias' object cannot resolve the original
name passed to its constructor during the '__set_name__' method.

- Attributes
  - 'owner': The owning class.
  - 'name': The name of the object in the owning class that could not be
  resolved.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class AliasException(Exception):
  """
  'AliasException' is raised when an 'Alias' object cannot resolve the
  original
  name passed to its constructor during the '__set_name__' method.

  - Attributes
    - 'owner': The owning class.
    - 'name': The name of the object in the owning class that could not be
      resolved.
  """

  owner = _Attribute()
  name = _Attribute()

  def __init__(self, owner: type, name: str) -> None:
    """Initialize the AliasException object."""
    self.owner = owner
    self.name = name

  def __eq__(self, other: object) -> bool:
    """Compare the AliasException object with another object."""
    if isinstance(other, AliasException):
      if self.owner is not other.owner:
        return False
      if self.name != other.name:
        return False
      return True
    otherOwner = getattr(other, '__field_owner__', None)
    otherName = getattr(other, '__field_name__', None)
    if otherOwner is None or otherName is None:
      return False
    if self.owner is not otherOwner:
      return False
    if self.name != otherName:
      return False
    return True

  def __str__(self) -> str:
    """Return a string representation of the AliasException object."""
    infoSpec = "Alias '%s' in '%s' could not resolve original name '%s'!"
    clsName = self.owner.__name__
    info = infoSpec % (self.name, clsName, self.name)
    return monoSpace(info)

  __repr__ = __str__
