"""
DuplicateKeeNum is a custom exception raised to indicate that a KeeNum
class received a duplicate entry for an enumeration.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class DuplicateKeeNum(Exception):
  """
  DuplicateKeeNum is a custom exception raised to indicate that a KeeNum
  class received a duplicate entry for an enumeration.
  """

  __slots__ = ('memberName', 'memberValue')

  def __init__(self, name: str, value: Any) -> None:
    """Initialize the DuplicateKeeNum object."""
    self.memberName = name
    self.memberValue = value
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    """Return the string representation of the DuplicateKeeNum object."""
    infoSpec = """Duplicate KeeNum member '%s' with value '%s'!"""
    info = infoSpec % (self.memberName, str(self.memberValue))
    return textFmt(info)

  __repr__ = __str__
