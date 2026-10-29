"""
NotAliasable is raised when an 'Alias' is bound in a class body to a name
the class holds as a descriptor it does not read as itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class NotAliasable(WorkToyException, SyntaxError):
  """
  NotAliasable is raised as a class is created when an 'Alias' in its
  body stands for a name the class holds as a descriptor it does not read
  as itself: a 'staticmethod' reads as the function inside it, a
  'classmethod' as a method bound to the class, a 'Dispatcher' as its
  compiled function. The alias forwards each access to what the class
  holds, so the two names would not agree on what the class gives. An
  alias stands for a descriptor the class reads as itself, such as an
  'AttriBox' or a 'Field', or for a plain function. A name no class holds
  is refused with 'DanglingAlias' instead. It subclasses 'SyntaxError', as
  the other refusals of a class-body line do.

  Attributes
  ----------
  alias : Any
    The 'Alias' that was refused.
  realName : str
    The name the alias stands for.
  held : Any
    What the class holds under that name, as the class dict has it.
  read : Any
    What reading the name from the class gives instead.
  """

  __slots__ = ('alias', 'realName', 'held', 'read')

  def __init__(
      self,
      alias: Any,
      realName: str,
      held: Any,
      read: Any
      ) -> None:
    self.alias = alias
    self.realName = realName
    self.held = held
    self.read = read
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The alias at '%s.%s' stands for '%s', which the class holds
    as a '%s' but reads as a '%s', so the two names would not agree. An
    alias stands for a descriptor the class reads as itself, such as an
    'AttriBox'."""
    try:
      owner = object.__getattribute__(self.alias, '__field_owner__')
    except AttributeError:
      owner = None
    ownerName = getattr(owner, '__name__', 'object')
    try:
      aliasName = object.__getattribute__(self.alias, '__field_name__')
    except AttributeError:
      aliasName = 'alias'
    names = (
      ownerName, aliasName, self.realName,
      type(self.held).__name__, type(self.read).__name__,
    )
    return textFmt(spec % names)

  __repr__ = __str__
