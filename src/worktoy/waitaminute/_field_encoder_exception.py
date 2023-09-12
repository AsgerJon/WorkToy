"""WorkToy - Wait A Minute - FieldEncoderException
Custom exception raised when an instance of 'DataField' attempts to
serialize its value to JSON format, but where the value is not
serializable.

When using DataField to describe instances of custom classes, use the
'DataField.ENCODER' and 'DataField.DECODER' to decorate functions defining
encoding and decoding respectively."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept

from worktoy.descriptors import DataField


class FieldEncoderException(MetaXcept):
  """WorkToy - Wait A Minute - FieldEncoderException"""

  def __init__(self, field: DataField, value: Any, owner: type,
               e: Exception, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._field = self.pretty(field)
    self._value = self.pretty(value)
    self._owner = self.pretty(owner)
    self._exception = self.pretty(e)

  def __str__(self) -> str:
    """Custom error message"""
    header = MetaXcept.__str__(self)
    field = self._field
    fieldName = 'unnamed'
    if isinstance(field, DataField):
      fieldName = field.getFieldName()
    value = self._value
    valueType = type(value)
    owner = self._owner
    body = """Default encoder failed to encode value of type %s 
    encountering the following exception: %s\n
    
    The field %s on %s describes a custom class, 
    but does not provide a custom encoding function."""
    msg = body % (valueType, self._exception, fieldName, owner)
    return '%s\n%s' % (header, self.justify(msg))
