"""
WithoutException is raised when a context-only descriptor method is used
outside any active descriptor context.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class WithoutException(WorkToyException, RuntimeError):
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
    #  The owner tells a placed descriptor apart: 'getFieldName' always
    #  answers, falling back to the name of the descriptor class.
    owner = self.desc.getFieldOwner()
    if owner is None:
      return infoSpec % ('NO-OWNER', 'NO-FIELD')
    return infoSpec % (owner.__name__, self.desc.getFieldName())

  __repr__ = __str__
