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
  KeeFlagDuplicate is raised when a 'KeeFlags' class body declares the same
  'KeeFlag' member name twice, or inherits a flag whose name collides with
  one declared on the subclass.

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

  def __init__(self, name: str, *members: Kee) -> None:
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
