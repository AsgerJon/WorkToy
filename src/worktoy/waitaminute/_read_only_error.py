"""ReadOnlyError is raised when an attempt is made to modify a read-only
attribute. This is a subclass of TypeError and should be used to indicate
that the attribute is read-only. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute, BadSet

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self


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
    self.existingValue, self.newValue = [*values, None, None][:2]
    fieldOwner = getattr(instance, '__field_owner__', None)
    fieldName = getattr(desc, '__field_name__', None)
    if fieldOwner is None or fieldName is None:
      info = """Cannot set value on ReadOnly attribute!"""
    else:
      fieldId = '%s.%s' % (fieldOwner.__name__, fieldName)
      newStr = str(self.newValue)
      if isinstance(self.newValue, BadSet):
        infoSpec = """Attempted to overwrite read-only attribute '%s'
        with new value: '%s'!"""
        info = infoSpec % (fieldId, newStr)
      else:
        oldStr = str(self.existingValue)
        infoSpec = """Attempted to overwrite read-only attribute '%s' 
        having value: '%s' with new value: '%s'!"""
        info = infoSpec % (fieldId, oldStr, newStr)

    TypeError.__init__(self, info)

  def _resolveOther(self, other: object) -> Self:
    """Resolve the other object."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, (tuple, list)):
      try:
        return cls(*other)
      except TypeError:
        return NotImplemented
    return NotImplemented

  def __eq__(self, other: object) -> bool:
    """Compare the ReadOnlyError object with another object."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    cls = type(self)
    if isinstance(other, cls):
      if self.owningInstance != other.owningInstance:
        return False
      if self.descriptorObject != other.descriptorObject:
        return False
      if self.existingValue != other.existingValue:
        return False
      if self.newValue != other.newValue:
        return False
      return True
    return False
