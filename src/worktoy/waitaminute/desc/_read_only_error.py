"""ReadOnlyError is raised when an attempt is made to modify a read-only
attribute. This is a subclass of TypeError and should be used to indicate
that the attribute is read-only. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import DescriptorException
from ...utilities import textFmt

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ReadOnlyError(DescriptorException):
  """ReadOnlyError is raised when an attempt is made to modify a read-only
  attribute. This is a subclass of TypeError and should be used to indicate
  that the attribute is read-only. """

  __slots__ = ('instance', 'desc', 'newVal',)

  def __init__(self, desc: Any, val: Any) -> None:
    """Initialize the ReadOnlyError."""
    self.instance = desc.__context_instance__
    self.desc = desc
    self.newVal = val
    DescriptorException.__init__(self, )

  def __str__(self, ) -> str:
    """Return the string representation of the ReadOnlyError."""
    infoSpec = """Attempted to overwrite read-only attribute '%s' with 
    new value: '%s'!"""
    ownerName = type(self.instance).__name__
    fieldName = getattr(self.desc, '__field_name__', 'object')
    fieldId = '%s.%s' % (ownerName, fieldName)
    newValue = str(self.newVal)
    info = infoSpec % (fieldId, newValue)
    return textFmt(info)

  __repr__ = __str__
