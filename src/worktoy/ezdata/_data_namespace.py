"""DataNamespace provides the namespace object for the DataMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.desc import AttriBox
from worktoy.meta import AbstractNamespace
from worktoy.parse import maybe
from worktoy.text import typeMsg


class DataNamespace(AbstractNamespace):
  """DataNamespace provides the namespace object for the DataMetaclass."""

  __data_fields__ = None

  def _initFactory(self, ) -> Callable:
    """Factory function for the __init__ method"""

    dataFields = self.getDataFields()

    def newInit(this, *args, **kwargs) -> None:
      """The newInit method is the __init__ method for the class."""
      for (arg, (key, field)) in zip(args, dataFields.items()):
        setattr(this, key, arg)
      for (key, field) in dataFields.items():
        if key in kwargs:
          val = kwargs[key]
          setattr(this, key, val)

    return newInit

  def getDataFields(self) -> dict[str, AttriBox]:
    """The getDataFields method returns the data fields."""
    dataFields = maybe(self.__data_fields__, {})
    if isinstance(dataFields, dict):
      for (key, val) in dataFields.items():
        if not isinstance(key, str):
          e = typeMsg('key', key, str)
          raise TypeError(e)
        if not isinstance(val, AttriBox):
          e = typeMsg('val', val, AttriBox)
          raise TypeError(e)
      return dataFields
    e = typeMsg('dataFields', dataFields, dict)
    raise TypeError(e)

  def _appendDataField(self, key: str, attriBox: AttriBox) -> None:
    """Appends the AttriBox instance at the given key."""
    existing = self.getDataFields()
    if key in existing:
      e = """Name conflict at name: '%s'!""" % key
      raise NameError(e)
    if not isinstance(attriBox, AttriBox):
      e = typeMsg('attriBox', attriBox, AttriBox)
      raise TypeError(e)
    self.__data_fields__ = {**existing, key: attriBox}

  def __explicit_set__(self, key: str, value: object) -> None:
    """The __setitem__ hook collects AttriBox instances. """
    if key == '__init__':
      e = """Reimplementing __init__ is not allowed for EZData classes!"""
      raise AttributeError(e)
    if isinstance(value, AttriBox):
      self._appendDataField(key, value)

  def compile(self, ) -> dict[str, object]:
    """The compile method returns the class namespace."""
    out = {}
    for (key, val) in dict.items(self):
      out[key] = val
    out['__init__'] = self._initFactory()
    return out
