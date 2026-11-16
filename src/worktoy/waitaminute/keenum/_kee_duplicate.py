"""
KeeDuplicate is raised when a 'KeeNum' class body declares two members
under the same name, or under names that differ only by case.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from ...keenum import Kee


class KeeDuplicate(WorkToyException, Exception):
  """
  Raised on a member name collision in a 'KeeNum' enumeration: either a
  class body that declares the same name twice, or a subclass that
  redeclares a name it already inherits (overriding an inherited member is
  not allowed). This is a name collision, not a value collision; duplicate
  values are allowed.

  Two names that differ only by case collide as well, since a lookup by
  name ignores case and could not tell their members apart: 'MW' beside
  'mW' in a class declared with 'strictCase=False', a subclass adding
  'MW' to an inherited 'mw', or two bases holding such a pair.

  The refusal comes while the class body runs, or before it, so the
  enumeration does not exist yet and is given by its name.

  Attributes
  ----------
  clsName : str
    The name of the enumeration class under construction.
  name : str
    The member name that was refused.
  oldMember : Kee
    The member already registered under 'name', or under a name that
    differs from it by case alone.
  newMember : Kee
    The member whose registration was rejected.
  """

  __slots__ = ('clsName', 'name', 'oldMember', 'newMember',)

  def __init__(self, clsName: str, name: str, *members: Kee) -> None:
    self.clsName = clsName
    self.name = name
    self.oldMember = members[0]
    self.newMember = members[1]
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Enumeration '%s' already contains member: '%s', and
    cannot take another member named '%s'! The names of the members of an
    enumeration must differ by more than their case, since a lookup by
    name ignores case."""
    oldStr = str(self.oldMember)
    info = infoSpec % (self.clsName, oldStr, self.name,)
    return textFmt(info)

  __repr__ = __str__
