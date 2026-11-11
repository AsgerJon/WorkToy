"""
KeeFlagDuplicate is raised on a flag name collision in a 'KeeFlags'
enumeration, whether in the class body or against an inherited flag.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from ...keenum import KeeFlag


class KeeFlagDuplicate(WorkToyException, Exception):
  """
  Raised on a flag name collision in a 'KeeFlags' enumeration: a class
  body that declares the same flag name twice, a subclass that declares
  a flag name it already inherits, or two bases holding two different
  flags of one name. The 'KeeFlags' counterpart to 'KeeDuplicate';
  neither family allows redeclaring an inherited name.

  Attributes
  ----------
  name : str
    The flag name that was declared more than once.
  oldFlag : Any
    What holds the name already: the declaration, a 'Kee' or a
    'KeeFlag', of a flag of the body, or the flag member of a base.
  newFlag : Any
    The declaration, or the flag member of a base, refused at the name.
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
