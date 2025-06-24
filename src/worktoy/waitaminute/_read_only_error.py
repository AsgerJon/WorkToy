"""ReadOnlyError is raised when an attempt is made to modify a read-only
attribute. This is a subclass of TypeError and should be used to indicate
that the attribute is read-only. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import _Attribute
from ..text import monoSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ReadOnlyError(TypeError):
  """ReadOnlyError is raised when an attempt is made to modify a read-only
  attribute. This is a subclass of TypeError and should be used to indicate
  that the attribute is read-only. """

  owningInstance = _Attribute()
  descriptorObject = _Attribute()
  existingValue = _Attribute()
  newValue = _Attribute()

  def __init__(self, instance: Any, desc: Any, *values) -> None:
    """Initialize the ReadOnlyError."""
    self.owningInstance = instance
    self.descriptorObject = desc
    self.newValue, self.existingValue = [*values, None, None][:2]
    TypeError.__init__(self, )

  def __str__(self, ) -> str:
    """Return the string representation of the ReadOnlyError."""
    infoSpec = """Attempted to overwrite read-only attribute '%s' 
    having value: '%s' with new value: '%s'!"""
    ownerName = type(self.owningInstance).__name__
    fieldName = getattr(self.descriptorObject, '__field_name__', 'object')
    fieldId = '%s.%s' % (ownerName, fieldName)
    oldValue = str(self.existingValue)
    newValue = str(self.newValue)
    info = infoSpec % (fieldId, oldValue, newValue)
    return monoSpace(info)

  __repr__ = __str__
