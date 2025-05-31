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

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never


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
    info = "Alias '%s' in '%s' could not resolve original name '%s'!"
    Exception.__init__(self, info % (name, owner.__name__, name))

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
