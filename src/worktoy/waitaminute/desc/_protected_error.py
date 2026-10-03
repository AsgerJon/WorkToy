"""
ProtectedError is raised on an attempt to delete a protected attribute.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescriptorException
from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ProtectedError(DescriptorException, AttributeError):
  """
  ProtectedError is raised on an attempt to delete a protected attribute.
  The default 'Object.__instance_delete__' raises it, as does any
  descriptor whose protocol forbids deletion, 'QuickDesc' included. It
  subclasses 'DescriptorException' and 'AttributeError', as 'AccessError'
  does: a specific type caught by its own name, which code catching
  'AttributeError' for a refused deletion, as Python raises for one,
  catches as well.

  Attributes
  ----------
  instance : Any
    The instance whose attribute the caller tried to delete.
  desc : Any
    The protected descriptor that rejected the deletion.
  oldVal : Any
    The value held before the deletion attempt, if known.
  """

  __slots__ = ('instance', 'desc', 'oldVal')

  def __init__(self, instance: Any, desc: Any, oldValue: Any = None) -> None:
    self.instance = instance
    self.desc = desc
    self.oldVal = oldValue
    DescriptorException.__init__(self, )

  def __str__(self, ) -> str:
    oldValue = self.oldVal
    desc = self.desc
    ownerName = type(self.instance).__name__
    fieldName = getattr(desc, '__field_name__', 'object')
    infoSpec = """Attempted to delete protected attribute '%s.%s'
      with value: '%s'"""
    info = infoSpec % (ownerName, fieldName, str(oldValue))
    return textFmt(info)

  __repr__ = __str__
