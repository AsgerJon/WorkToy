"""WorkToy - Wait A Minute - FieldDecoderException
Custom exception raised when an instance of 'DataField' attempts to decode
with default JSON decoder. The exception catches the JSONDecodeError and
brings additional information.

When using DataField to describe instances of custom classes, use the
'DataField.ENCODER' and 'DataField.DECODER' to decorate functions defining
encoding and decoding respectively."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.descriptors import DataField
from worktoy.waitaminute import MetaXcept


class FieldDecoderException(MetaXcept):
  """WorkToy - Wait A Minute - FieldDecoderException"""

  def __init__(self, field: DataField, data: str, owner: type,
               jsonDecodeException: Exception, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)

    self._field = self.pretty(field)
    self._value = self.pretty(data)
    self._owner = self.pretty(owner)
    self._exception = self.pretty(jsonDecodeException)

  def __str__(self) -> str:
    """Custom error message"""
    header = MetaXcept.__str__(self)
    body = """Default encoder failed to decode the data: \n%s\n but 
    encountered: %s!\n
    DataField %s on %s does not specify a custom decoder which is 
    recommended."""
    msg = body % (self._value, self._exception, self._field, self._owner)
    return '%s\n%s' % (header, self.justify(msg))
