"""
KeeDuplicate is raised when a 'KeeNum' class body declares two members
under the same name.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from ...keenum import Kee


class KeeDuplicate(Exception):
  """
  Raised when a 'KeeNum' class body declares two members under the same
  name (a name collision, not a value collision; duplicate values are
  allowed).

  Attributes
  ----------
  name : str
    The member name declared more than once.
  oldMember : Kee
    The member already registered under 'name'.
  newMember : Kee
    The member whose registration was rejected.
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
