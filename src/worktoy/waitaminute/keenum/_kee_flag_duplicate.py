"""
KeeFlagDuplicate is a custom exception raised to indicate that a KeeFlags
class received a duplicate entry for an enumeration.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeeFlagDuplicate(Exception):
  """
  KeeDuplicate is a custom exception raised to indicate that a KeeNum
  class received a duplicate entry for an enumeration.
  """

  __slots__ = ('name', 'oldFlag', 'newFlag',)

  def __init__(self, name: str, *members: Kee) -> None:
    """Initialize the KeeDuplicate object."""
    self.name = name
    self.oldFlag = members[0]
    self.newFlag = members[1]
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    """Return the string representation of the KeeDuplicate object."""
    infoSpec = """Enumeration name '%s' already contains flag: '%s', 
    but attempted to add duplicate: '%s'!"""
    oldStr = str(self.oldFlag)
    newStr = str(self.newFlag)
    info = infoSpec % (self.name, oldStr, newStr,)
    return textFmt(info)

  __repr__ = __str__
