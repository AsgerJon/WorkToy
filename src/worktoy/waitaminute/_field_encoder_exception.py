"""WorkToy - Wait A Minute - FieldEncoderException
Custom exception raised when an instance of 'DataField' attempts to
serialize its value to JSON format, but where the value is not
serializable.

When using DataField to describe instances of custom classes, use the
'DataField.ENCODER' and 'DataField.DECODER' to decorate functions defining
encoding and decoding respectively."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept

from workside.moreworktoy import DataField


class FieldEncoderException(MetaXcept):
  """WorkToy - Wait A Minute - FieldEncoderException"""

  def __init__(self, field: DataField, value: Any, owner: type,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._field = self.pretty(field)
    self._value = self.pretty(value)
    self._owner = self.pretty(owner)

  def __str__(self) -> str:
    """Custom error message"""
