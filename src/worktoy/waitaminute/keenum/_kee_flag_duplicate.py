"""
KeeFlagDuplicate is raised on a flag name collision in a 'KeeFlags'
enumeration, whether in the class body or against an inherited flag.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from ...keenum import KeeFlag


class KeeFlagDuplicate(Exception):
  """
  Raised on a flag name collision in a 'KeeFlags' enumeration: either a
  class body that declares the same 'KeeFlag' name twice, or a subclass
  that redeclares a flag name it already inherits. The 'KeeFlags'
  counterpart to 'KeeDuplicate'; neither family allows redeclaring an
  inherited name.

  Attributes
  ----------
  name : str
    The flag name that was declared more than once.
  oldFlag : KeeFlag
    The flag already registered under that name.
  newFlag : KeeFlag
    The flag whose duplicate registration was rejected.
  """

  __slots__ = ('name', 'oldFlag', 'newFlag',)

  def __init__(self, name: str, *members: KeeFlag) -> None:
    self.name = name
    self.oldFlag = members[0]
    self.newFlag = members[1]
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Enumeration name '%s' already contains flag: '%s', 
    but attempted to add duplicate: '%s'!"""
    oldStr = str(self.oldFlag)
    newStr = str(self.newFlag)
    info = infoSpec % (self.name, oldStr, newStr,)
    return textFmt(info)

  __repr__ = __str__
