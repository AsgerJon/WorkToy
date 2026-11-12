"""
KeeWriteOnceError is raised on an attempt to modify a member of a
'KeeNum' or 'KeeFlags' class after initialization, or to rebind or
delete the name of a member on the class.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class KeeWriteOnceError(WorkToyException, AttributeError):
  """
  KeeWriteOnceError provides a custom exception raised to indicate attempt
  to modify a member of a 'KeeNum' enumeration or of a 'KeeFlags' class.
  All such members are write-once, disallowing any and all modifications
  after initialization. The same exception refuses rebinding or deleting
  the name of a member on a class of either kind.

  Note: A member reads its 'value' from its declaration once, as it is
  built, and nothing sets it at a later access; all enumeration members
  are strictly write-once.
  """

  __slots__ = ('keeNum', 'member', 'attribute')

  def __init__(self, member: Any, attribute: str) -> None:
    self.keeNum = type(member)
    self.member = member
    self.attribute = attribute

  def __str__(self) -> str:
    infoSpec = """Attempt to modify attribute '%s' of member '%s' in '%s'!"""
    key = self.attribute
    num = str(self.member)
    kee = self.keeNum.__name__
    info = infoSpec % (key, num, kee)
    from ...utilities import textFmt
    return textFmt(info)

  __repr__ = __str__
