"""
KeeNameConflict provides a custom exception raised to indicate that a
'KeeNum' enumeration received a 'Kee' member reservation already named,
but provided at a different name.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

  from ...keenum import Kee


class KeeNameConflict(ValueError):
  """
  KeeNameConflict provides a custom exception raised to indicate that a
  'KeeNum' enumeration received a 'Kee' member reservation already named,
  but provided at a different name.
  """

  member: Any
  oldName: str
  newName: str

  __slots__ = ('__kee_object__', '__existing_name__', '__new_name__',)

  def __init__(self, kee: Kee, oldName: str, newName: str) -> None:
    """Initialize the KeeNameConflict object."""
    self.member = kee
    self.oldName = oldName
    self.newName = newName
    ValueError.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Name conflict for Kee member object '%s': existing name 
    '%s' versus new name '%s'!"""
    keeName = getattr(self.member, '__name__', 'Unknown')
    info = infoSpec % (keeName, self.oldName, self.newName,)
    return info

  __repr__ = __str__
