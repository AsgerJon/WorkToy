"""FastSpace provides the namespace object class for the FastObject class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace, typeMsg

try:
  from typing import Callable
except ImportError:
  Callable = object

from worktoy.desc import AttriBox
from worktoy.meta import BaseNamespace
from worktoy.parse import maybe


class FastSpace(BaseNamespace):
  """EZSpace provides the namespace object class for the EZData class."""

  __field_boxes__ = None
  __inner_functions__ = None

  def __init__(self, *args, **kwargs) -> None:
    """The '__init__' method initializes the namespace object."""
    BaseNamespace.__init__(self, *args, **kwargs)
    baseClasses = self.getBaseClasses()
    if len(baseClasses) > 1:
      mclsName = self.getMetaClass().__name__
      name = self.getClassName()
      spaceName = self.__class__.__name__
      baseNames = ', '.join([b.__name__ for b in baseClasses])
      e = """When trying to create a new class named: '%s' derived from 
      metaclass: '%s', the namespace object of type '%s' supports only 
      single inheritance! Nevertheless, the following base classes were
      provided: (%s)!"""
      e2 = e % (name, mclsName, spaceName, baseNames)
      raise ValueError(monoSpace(e2))

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

  def _getBaseBoxes(self) -> list[tuple[str, AttriBox]]:
    """This method returns the base field boxes."""
    baseClasses = self.getBaseClasses()
    if not baseClasses:
      return []
    baseCls = self.getBaseClasses()[0]
    baseBoxes = getattr(baseCls, '__field_boxes__', None)
    if baseBoxes is None:
      return []
    if isinstance(baseBoxes, list):
      return baseBoxes
    e = typeMsg('baseBoxes', baseBoxes, list)
    raise TypeError(e)

  def _getAllBoxes(self, ) -> list[tuple[str, AttriBox]]:
    """This method returns all the field boxes."""
    baseBoxes = self._getBaseBoxes()
    fieldBoxes = self._getFieldBoxes()
    return [*baseBoxes, *fieldBoxes]

  def _addFieldBox(self, key: str, box: AttriBox) -> None:
    """This method adds a field box to the namespace."""
    boxes = self._getFieldBoxes()
    self.__field_boxes__ = [*boxes, (key, box)]

  def __setitem__(self, key: str, value: object) -> None:
    """This method sets the key, value pair in the namespace."""
    if isinstance(value, AttriBox):
      return self._addFieldBox(key, value)
    if callable(value) or (key.startswith('__') and key.endswith('__')):
      return BaseNamespace.__setitem__(self, key, value)
    e = """Attributes are required to be instances of AttriBox, 
    but received '%s' of type '%s' at key: '%s'!"""
    e2 = e % (str(value), type(value).__name__, key)
    raise ValueError(monoSpace(e2))

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
        setattr(self, key, defGet[key](self))
      return object.__getattribute__(self, key)

    return __getattr__

  @staticmethod
  def _slotsFactory(boxes: list[tuple[str, AttriBox]]) -> list[str]:
    """This factory creates the '__slots__' list which is used to restrict
    the namespace to the AttriBox instances."""
    return [box[0] for box in boxes]

  def compile(self) -> dict:
    """The namespace created by the BaseNamespace class is updated with
    the '__init__' function created by the factory function."""
    namespace = BaseNamespace.compile(self)
    fieldBoxes = self._getFieldBoxes()
    baseBoxes = self._getBaseBoxes()
    bases = self.getBaseClasses()
    boxes = self._getAllBoxes()
    self._addInnerFunction('__getattr__', self._getattrFactory(boxes))
    namespace['__field_boxes__'] = self._getFieldBoxes()
    namespace['__slots__'] = self._slotsFactory(boxes)
    for (key, callMeMaybe) in self._getInnerFunctions():
      namespace[key] = callMeMaybe
    return namespace
