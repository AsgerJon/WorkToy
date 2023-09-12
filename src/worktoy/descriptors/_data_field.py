"""MoreWorkToy - DataField
Subclass of Field implementing json saving and loading along with the
accessor functions."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import json
from typing import Any

from icecream import ic
from worktoy.core import Function
from worktoy.descriptors import Field

ic.configureOutput(includeContext=True)


class DataField(Field):
  """MoreWorkToy - DataField
  Subclass of Field implementing json saving and loading along with the
  accessor functions."""

  def __init__(self, *args, **kwargs) -> None:
    Field.__init__(self, *args, **kwargs)
    self._encoderFunction = None
    self._decoderFunction = None

  def getDefaultEncoderFunction(self) -> Function:
    """Getter-function for the default encoder function. """

    def defaultEncoder(value: Any) -> str:
      """Default encoder. This default encoder attempts to
      encode with json.dumps. If it fails, the custom exception
      'FieldEncoderException' is raised. """
      try:
        return json.dumps(value)
      except TypeError as e:
        raise e

  def getDefaultDecoderFunction(self) -> Function:
    """Getter-function for the default decoder function. """

  def getEncoderFunction(self) -> Function:
    """Getter-function for the encoder function. """

  def getDecoderFunction(self) -> Function:
    """Setter-function for the decoder function. """

  def ENCODER(self, encoderFunction: Function) -> Function:
    """Sets the encoder function to the decorated function before returning
    it. """
    self.overRideGuard(
      self._encoderFunction, '_encoderFunction', encoderFunction)
    self._encoderFunction = encoderFunction
    return encoderFunction

  def DECODER(self, decoderFunction: Function) -> Function:
    """Sets the decoder function to the decorated function before returning
    it."""
    self.overRideGuard(
      self._decoderFunction, '_decoderFunction', decoderFunction)
    self._decoderFunction = decoderFunction
    return decoderFunction

  def setFieldOwner(self, cls: type) -> None:
    """Setter-function for the field owner."""
    Field.setFieldOwner(self, cls)
    existingDataFields = getattr(cls, '__data_fields__', {})
    existingDataFields |= {self.getFieldName(): self}
    setattr(cls, '__data_fields__', existingDataFields)

  def encode(self, obj: Any) -> str:
    """Encodes the field"""
    encoder = self.getEncoderFunction()

  def decode(self, obj: Any, data: str) -> None:
    """Decodes the data and applies to field on object."""
    value = None
    if isinstance(data, str):
      data = json.loads(data)
    if isinstance(data, dict):
      value = data.get(self.getFieldName(), None)
    return self._setterFunction(obj, value)

  def explicitGetter(self, obj: Any) -> Any:
    """Explicit getter function"""
    return self._getterFunction(obj)

  def explicitSetter(self, obj: Any, newValue: Any) -> Any:
    """Explicit getter function"""
    return self._setterFunction(obj, newValue)

  def explicitEncoder(self, value: Any) -> Any:
    """Explicit encoder. This method should return a 'str' from which the
    value can be decoded. """
