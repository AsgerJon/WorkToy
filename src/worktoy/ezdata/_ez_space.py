"""EZSpace provides the namespace object class for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg

try:
  from typing import Callable
except ImportError:
  Callable = object

from worktoy.desc import AttriBox
from worktoy.meta import BaseNamespace
from worktoy.parse import maybe


class EZSpace(BaseNamespace):
  """EZSpace provides the namespace object class for the EZData class."""

  __field_boxes__ = None

  def _getFieldBoxes(self) -> list[tuple[str, AttriBox]]:
    """This method returns the field boxes."""
    return maybe(self.__field_boxes__, [])

  def _addFieldBox(self, key: str, box: AttriBox) -> None:
    """This method adds a field box to the namespace."""
    boxes = self._getFieldBoxes()
    self.__field_boxes__ = [*boxes, (key, box)]

  def __setitem__(self, key: str, value: object) -> None:
    """This method sets the key, value pair in the namespace."""
    if self.getClassName() != 'EZData':
      if key == '__init__':
        e = """EZData subclasses are not permitted to implement the 
        '__init__' method!"""
        raise AttributeError(e)
    if isinstance(value, AttriBox):
      self._addFieldBox(key, value)
    BaseNamespace.__setitem__(self, key, value)

  @staticmethod
  def _initFactory(attriBoxes: list[tuple[str, AttriBox]]) -> Callable:
    """This factory creates the '__init__' method which automatically
    populates the AttriBox instances."""

    keys = [key for (key, box) in attriBoxes]
    boxes = [box for (key, box) in attriBoxes]

    def __init__(self, *args, **kwargs) -> None:
      """This automatically generated '__init__' method populates the
      AttriBox instances."""
      for box in boxes:
        if not isinstance(box, AttriBox):
          e = typeMsg('box', box, AttriBox)
          raise TypeError(e)
        box.silenceInstance(self)

      for (key, arg) in zip(keys, args):
        setattr(self, key, arg)

      for key in keys:
        if key in kwargs:
          setattr(self, key, kwargs[key])

      for box in boxes:
        box.unsilenceInstance(self)

    return __init__

  def compile(self) -> dict:
    """The namespace created by the BaseNamespace class is updated with
    the '__init__' function created by the factory function."""
    out = BaseNamespace.compile(self)
    boxes = self._getFieldBoxes()
    if boxes:
      out['__init__'] = self._initFactory(boxes)
    return out
