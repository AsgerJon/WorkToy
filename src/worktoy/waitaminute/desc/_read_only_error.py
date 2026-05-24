"""ReadOnlyError is raised on an attempt to assign to a read-only
attribute. It subclasses 'DescriptorException', the shared base for
descriptor failures. The default 'Object.__instance_set__' raises it, as
does any descriptor whose protocol forbids writes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescriptorException
from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ReadOnlyError(DescriptorException):
  """
  ReadOnlyError is raised on an attempt to assign to a read-only
  attribute. It subclasses 'DescriptorException' (and so 'Exception'). The
  default 'Object.__instance_set__' raises it, as does any descriptor
  whose protocol forbids writes.

  Attributes
  ----------
  instance : Any
    The instance whose attribute the caller tried to write.
  desc : Any
    The read-only descriptor that rejected the write.
  newVal : Any
    The value the caller tried to assign.
  """

  __slots__ = ('instance', 'desc', 'newVal',)

  def __init__(self, instance: Any, desc: Any, val: Any, ) -> None:
    self.instance = instance
    self.desc = desc
    self.newVal = val
    DescriptorException.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Attempted to overwrite read-only attribute '%s' with 
    new value: '%s'!"""
    ownerName = type(self.instance).__name__
    fieldName = getattr(self.desc, '__field_name__', 'object')
    fieldId = '%s.%s' % (ownerName, fieldName)
    newValue = str(self.newVal)
    info = infoSpec % (fieldId, newValue)
    return textFmt(info)

  __repr__ = __str__
