"""
KeeDuplicate is a custom exception raised to indicate that a KeeNum
class received a duplicate entry for an enumeration.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from ...keenum import Kee


class KeeDuplicate(Exception):
  """
  KeeDuplicate is a custom exception raised to indicate that a KeeNum
  class received a duplicate entry for an enumeration.
  """

  __slots__ = ('name', 'oldMember', 'newMember',)

  def __init__(self, name: str, *members: Kee) -> None:
    self.name = name
    self.oldMember = members[0]
    self.newMember = members[1]
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Enumeration name '%s' already contains member: '%s', 
    but attempted to add duplicate member: '%s'!"""
    oldStr = str(self.oldMember)
    newStr = str(self.newMember)
    info = infoSpec % (self.name, oldStr, newStr,)
    return textFmt(info)

  __repr__ = __str__
