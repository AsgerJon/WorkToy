"""MoreWorkToy - DataClass
Class decorator combining all DataFields on the class to one
encoder-decoder pair."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import json
from typing import Any

from icecream import ic
from worktoy.worktoyclass import WorkToyClass

from worktoy.descriptors import DataField

ic.configureOutput(includeContext=True)


class DataClass(WorkToyClass):
  """MoreWorkToy - DataClass
  Class decorator combining all DataFields on the class to one
  encoder-decoder pair."""

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self._innerClass = None

  def __call__(self, target: type) -> type:
    """Decorates the class. """

    if self._innerClass is not None:
      from worktoy.waitaminute import UnavailableNameException
      name = '_innerClass'
      oldVal = self._innerClass
      newVal = target
      raise UnavailableNameException(name, oldVal, newVal)

    self._innerClass = target

    def encodeAll(cls: type = None, obj: Any = None, ) -> str:
      """Creates a json string representation of all data fields defined
      on the class."""
      if self.empty(cls, obj):
        from worktoy.waitaminute import MissingArgumentException
        raise MissingArgumentException('obj')
      if obj is None:
        obj = cls
        cls = obj.__class__
      if not self.plenty(cls, obj):
        raise TypeError

      data = {}

      dataFields = getattr(cls, '__data_fields__', {})
      for fieldName, dataField in dataFields.items():
        if isinstance(dataField, DataField):
          value = dataField.explicitGetter(obj)
          encodedData = dataField.explicitEncoder(value)
          data |= {fieldName: encodedData}
      return json.dumps(data)

    def decodeAll(cls: type = None, data: str = None) -> Any:
      """Decodes data to new instance of decorated class"""
      if self.empty(cls, data):
        from worktoy.waitaminute import MissingArgumentException
        raise MissingArgumentException('cls')
      if data is None:
        data = cls
        cls = target

      obj = cls()

      dataFields = getattr(cls, '__data_fields__', {})
      data = json.loads(data)

      for fieldName, dataField in dataFields.items():
        encodedData = data.get(fieldName, None)
        if encodedData is None:
          raise ValueError
        value = dataField.explicitDecoder(encodedData)
        dataField.explicitSetter(obj, value)

      return obj

    setattr(target, 'encodeAll', encodeAll)
    setattr(target, 'decodeAll', decodeAll)
    setattr(target, '__data_class__', True)
    return target
