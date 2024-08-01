"""DataNamespace provides the namespace object for the DataMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from icecream import ic

from worktoy.desc import AttriBox
from worktoy.meta import AbstractNamespace
from worktoy.parse import maybe
from worktoy.text import typeMsg

ic.configureOutput(includeContext=True)


class DataNamespace(AbstractNamespace):
  """DataNamespace provides the namespace object for the DataMetaclass."""

  __data_fields__ = None
  __data_boxes__ = None
  __field_section__ = False

  def _initFactory(self, ) -> Callable:
    """Factory function for the __init__ method"""

    dataFields = self.getDataBoxes()

    def newInit(this, *args, **kwargs) -> None:
      """The newInit method is the __init__ method for the class."""
      boxes = this.getDataBoxes()
      boxDict = this.getDataBoxDict()
      for ((key, box), arg) in zip(boxes, args):
        cls = AttriBox.getFieldClass(box)
        if isinstance(arg, cls):
          setattr(this, key, arg)
          continue
        e = typeMsg('arg', arg, cls)
        raise TypeError(e)
      for (key, val) in kwargs.items():
        if key not in boxDict:
          continue
        box = boxDict[key]
        cls = AttriBox.getFieldClass(box)
        if isinstance(val, cls):
          setattr(this, key, val)
          continue
        e = typeMsg('val', val, cls)
        raise TypeError(e)

    return newInit

  def __setitem__(self, key: str, value: object) -> None:
    """The __setitem__ hook collects AttriBox instances. """
    if key == '__init__':
      e = """Reimplementing __init__ is not allowed for EZData classes!"""
      raise AttributeError(e)
    if isinstance(value, AttriBox):
      return self._appendDataBox(key, value)
    return dict.__setitem__(self, key, value)

  def getDataBoxes(self) -> list[tuple[str, AttriBox]]:
    """The getDataBoxes method returns the data boxes."""
    return maybe(self.__data_boxes__, [])

  def getDataBoxDict(self) -> dict[str, AttriBox]:
    """The getDataBoxDict method returns the data boxes as a dictionary."""
    return {k: v for (k, v) in self.getDataBoxes()}

  def _appendDataBox(self, key: str, box: AttriBox) -> None:
    """Appends the AttriBox instance at the given key."""
    existing = self.getDataBoxes()
    if key in existing:
      e = """Name conflict at name: '%s'!""" % key
      raise NameError(e)
    self.__data_boxes__ = [*existing, (key, box)]

  def compile(self, ) -> dict[str, object]:
    """The compile method returns the class namespace."""
    out = {k: v for (k, v) in self.getDataBoxes()}
    for (key, val) in dict.items(self):
      out[key] = val
    out['__init__'] = self._initFactory()
    out['__data_boxes__'] = self.getDataBoxes()
    if getattr(self.getDataBoxes, '__func__', None) is not None:
      getDataBoxesFunc = getattr(self.getDataBoxes, '__func__', None)
    else:
      getDataBoxesFunc = self.getDataBoxes
    if getattr(self.getDataBoxDict, '__func__', None) is not None:
      getDataBoxDictFunc = getattr(self.getDataBoxDict, '__func__', None)
    else:
      getDataBoxDictFunc = self.getDataBoxDict
    out['getDataBoxes'] = getDataBoxesFunc
    out['getDataBoxDict'] = getDataBoxDictFunc
    return out
