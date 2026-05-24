"""
WithoutException is raised when a context-only descriptor method is used
outside any active descriptor context, such as reading 'self.instance' or
calling 'exitContext' on 'Object' when no '(instance, owner)' frame is on
the context stack.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class WithoutException(RuntimeError):
  """
  WithoutException is raised when a context-only descriptor method is used
  outside any active descriptor context. 'Object' raises it when
  'self.instance' or 'self.owner' is read with no frame on the context
  stack, and when 'exitContext' is called on an empty stack (an unpaired
  'createContext' / 'exitContext').

  Attributes
  ----------
  desc : object
    The descriptor whose context was missing.
  """

  __slots__ = ('desc',)

  def __init__(self, desc: Any) -> None:
    self.desc = desc
    RuntimeError.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Context-less call detected for descriptor at '%s.%s'!"""
    fbOwner = 'NO-OWNER'
    ownerName = getattr(self.desc.getFieldOwner(), '__name__', fbOwner)
    fbName = 'NO-FIELD'
    from worktoy.utilities import maybe
    fieldName = maybe(self.desc.getFieldName(), fbName)
    info = infoSpec % (ownerName, fieldName)
    return info

  __repr__ = __str__
