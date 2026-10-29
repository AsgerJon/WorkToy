"""
NotADescriptor is raised when an 'Alias' stands for a name that holds
something other than a descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class NotADescriptor(WorkToyException, TypeError):
  """
  NotADescriptor is raised when an 'Alias' stands for a name that holds
  something other than a descriptor, such as a plain value assigned to
  the class. The alias forwards to the descriptor the real name holds,
  and a plain value has no protocol to forward to; it takes a second name
  by plain assignment instead. It subclasses 'TypeError', so the refusal
  is loud where an 'AttributeError' would read as the attribute being
  absent.

  Attributes
  ----------
  alias : Any
    The 'Alias' whose access was refused.
  realName : str
    The name the alias stands for.
  found : Any
    What that name holds.
  """

  __slots__ = ('alias', 'realName', 'found')

  def __init__(self, alias: Any, realName: str, found: Any) -> None:
    self.alias = alias
    self.realName = realName
    self.found = found
    TypeError.__init__(self, )

  def __str__(self) -> str:
    spec = """The name '%s.%s' stands for '%s', which holds '%s' of type
    '%s' rather than a descriptor. An alias names a descriptor such as an
    'AttriBox'; a plain value takes a second name by assignment."""
    try:
      owner = object.__getattribute__(self.alias, '__field_owner__')
    except AttributeError:
      owner = None
    ownerName = getattr(owner, '__name__', 'object')
    try:
      aliasName = object.__getattribute__(self.alias, '__field_name__')
    except AttributeError:
      aliasName = 'alias'
    foundStr = repr(self.found)
    if len(foundStr) > 50:
      foundStr = '%s...' % foundStr[:47]
    names = (
      ownerName, aliasName, self.realName, foundStr,
      type(self.found).__name__,
    )
    return textFmt(spec % names)

  __repr__ = __str__
