"""
DanglingAlias is raised when an 'Alias' stands for a name that no class
along the resolution order of its owner holds.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class DanglingAlias(WorkToyException, SyntaxError):
  """
  DanglingAlias is raised when an 'Alias', or a reference through 'THIS'
  such as 'THIS[Parent].x', stands for a name that no class along the
  resolution order holds: that of the owner for an alias, that of the
  class named for a reference. Both forward to the descriptor the real
  name holds, so a name nobody holds leaves them nothing to forward to.
  The refusal comes at the line for a reference, as the class is created
  for an alias, and for an alias again from an access should the name be
  removed from the class afterwards. It subclasses 'SyntaxError', as the
  other refusals of a class-body line do.

  Attributes
  ----------
  alias : Any
    The 'Alias' or 'THIS' reference that was refused.
  realName : str
    The name the alias stands for.
  owner : type
    The class whose resolution order was searched.
  """

  __slots__ = ('alias', 'realName', 'owner')

  def __init__(self, alias: Any, realName: str, owner: type) -> None:
    self.alias = alias
    self.realName = realName
    self.owner = owner
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The name '%s.%s' stands for '%s', which no class along the
    resolution order of '%s' holds. An alias, or a decoration through
    'THIS', stands for a descriptor the class already holds, such as an
    'AttriBox'."""
    ownerName = getattr(self.owner, '__name__', 'object')
    try:
      aliasName = object.__getattribute__(self.alias, '__field_name__')
    except AttributeError:
      aliasName = 'alias'
    names = (ownerName, aliasName, self.realName, ownerName)
    return textFmt(spec % names)

  __repr__ = __str__
