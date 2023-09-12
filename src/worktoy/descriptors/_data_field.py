"""MoreWorkToy - DataField
Subclass of Field implementing json saving and loading along with the
accessor functions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import json
from json import JSONDecodeError
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
        from worktoy.waitaminute import FieldEncoderException
        field = self
        owner = self.getFieldOwner()
        raise FieldEncoderException(field, value, owner, e)

    return defaultEncoder

  def getDefaultDecoderFunction(self) -> Function:
    """Getter-function for the default decoder function. """

    def defaultDecoder(data: str) -> Any:
      """Default decoder. This default decoder attempts to decode with
      json.loads. If it fails, the custom exception FieldDecoderException
      is raised."""
      try:
        return json.loads(data)
      except JSONDecodeError as e:
        from worktoy.waitaminute import FieldDecoderException
        field = self
        owner = self.getFieldOwner()
        raise FieldDecoderException(field, data, owner, e)

    return defaultDecoder

  def getEncoderFunction(self) -> Function:
    """Getter-function for the encoder function. """

    if self._encoderFunction is None:
      return self.getDefaultEncoderFunction()
    return self._encoderFunction

  def getDecoderFunction(self) -> Function:
    """Setter-function for the decoder function. """

    if self._decoderFunction is None:
      return self.getDefaultDecoderFunction()
    return self._decoderFunction

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

  def encode(self, value: Any) -> str:
    """Encodes the field"""
    encoder = self.getEncoderFunction()
    return encoder(value)

  def decode(self, encodedData: str) -> None:
    """Decodes the data and applies to field on object."""
    decoder = self.getDecoderFunction()
    return decoder(encodedData)

  def explicitGetter(self, obj: Any) -> Any:
    """Explicit getter function"""
    return self._getterFunction(obj)

  def explicitSetter(self, obj: Any, newValue: Any) -> Any:
    """Explicit getter function"""
    return self._setterFunction(obj, newValue)

  def explicitEncoder(self, value: Any) -> str:
    """Explicit encoder. This method should return a 'str' from which the
    value can be decoded. """

    encoder = self.getEncoderFunction()
    return encoder(value)

  def explicitDecoder(self, data: str) -> Any:
    """Explicit decoder. This method receives a 'str' from which it should
    decode a value of the DataField type."""

    decoder = self.getDecoderFunction()
    return decoder(data)
