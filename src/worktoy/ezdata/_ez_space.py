"""EZSpace provides the namespace object class for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg, monoSpace

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
  __inner_functions__ = None

  def _getInnerFunctions(self) -> list[tuple[str, Callable]]:
    """This method returns the inner functions."""
    return maybe(self.__inner_functions__, [])

  def _addInnerFunction(self, key: str, func: Callable) -> None:
    """This method adds an inner function to the namespace."""
    funcs = self._getInnerFunctions()
    self.__inner_functions__ = [*funcs, (key, func)]

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
    elif callable(value):
      self._addInnerFunction(key, value)
    elif key.startswith('__') and key.endswith('__'):
      BaseNamespace.__setitem__(self, key, value)
    else:
      e = """EZData subclasses are only permitted to have AttriBox
      attributes and callables in their namespace, but received:
      '%s' of type '%s' at key: '%s'!""" % (value, type(value).__name__, key)
      raise AttributeError(monoSpace(e))

  @staticmethod
  def _initFactory(attriBoxes: list[tuple[str, AttriBox]]) -> Callable:
    """This factory creates the '__init__' method which automatically
    populates the AttriBox instances."""

    keys = [key for (key, box) in attriBoxes]

    def __init__(self, *args, **kwargs) -> None:
      """This automatically generated '__init__' method populates the
      AttriBox instances."""

      popKeys = []

      for (key, arg) in zip(keys, args):
        setattr(self, key, arg)
        popKeys.append(key)

      for key in keys:
        if key in kwargs:
          setattr(self, key, kwargs[key])
          if key not in popKeys:
            popKeys.append(key)

    return __init__

  @staticmethod
  def _getattrFactory(boxes: list[tuple[str, AttriBox]]) -> Callable:
    """This factory creates the '__getattr__' method which automatically
    retrieves the AttriBox instances."""

    keys = [key for (key, box) in boxes]
    defGet = {key: box.getDefaultFactory() for (key, box) in boxes}

    def __getattr__(self, key: str) -> object:
      """This automatically generated '__getattr__' method retrieves the
      AttriBox instances."""
      if key in defGet:
        setattr(self, key, defGet[key]())
      return object.__getattribute__(self, key)

    return __getattr__

  @staticmethod
  def _slotsFactory(boxes: list[tuple[str, AttriBox]]) -> list[str]:
    """This factory creates the '__slots__' list which is used to restrict
    the namespace to the AttriBox instances."""
    return [key for (key, box) in boxes]

  def compile(self) -> dict:
    """The namespace created by the BaseNamespace class is updated with
    the '__init__' function created by the factory function."""
    boxes = self._getFieldBoxes()
    if boxes:
      __init__ = self._initFactory(boxes)
      __getattr__ = self._getattrFactory(boxes)
      self._addInnerFunction('__init__', __init__)
      self._addInnerFunction('__getattr__', __getattr__)
    namespace = BaseNamespace.compile(self)
    namespace['__slots__'] = self._slotsFactory(boxes)
    for (key, callMeMaybe) in self._getInnerFunctions():
      namespace[key] = callMeMaybe
    return namespace
