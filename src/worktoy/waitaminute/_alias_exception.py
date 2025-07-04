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

from ..utilities import textFmt

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class AliasException(RuntimeError):
  """
  'AliasException' is raised when an 'Alias' object cannot resolve the
  original
  name passed to its constructor during the '__set_name__' method.

  - Attributes
    - 'owner': The owning class.
    - 'name': The name of the object in the owning class that could not be
      resolved.
  """

  __slots__ = ("owner", "name")

  def __init__(self, owner: type, name: str) -> None:
    """Initialize the AliasException object."""
    self.owner = owner
    self.name = name
    RuntimeError.__init__(self, )

  def __str__(self) -> str:
    """Return a string representation of the AliasException object."""
    infoSpec = "Alias '%s' in '%s' could not resolve original name '%s'!"
    clsName = self.owner.__name__
    info = infoSpec % (self.name, clsName, self.name)
    return textFmt(info)

  __repr__ = __str__
