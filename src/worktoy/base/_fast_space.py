"""FastSpace provides the namespace object class for the FastObject class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg

try:
  from typing import Callable, Any, Self
except ImportError:
  Callable = object
  Any = object
  Self = object

from worktoy.desc import AttriBox, ExplicitBox
from worktoy.meta import OverloadSpace, Overload
from worktoy.parse import maybe


class FastSpace(OverloadSpace):
  """EZSpace provides the namespace object class for the EZData class."""

  __field_boxes__ = None
  __inner_functions__ = None

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
    if callable(value) or isinstance(value, Overload):
      return OverloadSpace.__setitem__(self, key, value)
    if self.isSpecialKey(key):
      return dict.__setitem__(self, key, value)
    return self.__setitem__(key, ExplicitBox[type(value)](value))

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
  def _initFactory(attriBoxes: list[tuple[str, AttriBox]]) -> Callable:
    """This factory creates the '__init__' method which automatically
    populates the AttriBox instances."""

    keys = [key for (key, box) in attriBoxes]
    defVals = {key: box.getDefaultFactory() for (key, box) in attriBoxes}
    valTypes = {key: box.getFieldClass() for (key, box) in attriBoxes}

    def __init__(self, *args, **kwargs) -> None:
      """This automatically generated '__init__' method populates the
      AttriBox instances."""
      initValues = dict()  # Creates temporary dictionary for initial values

      #  Retrieves values from positional arguments
      for (i, (key, type_)) in enumerate(valTypes.items()):
        if len(args) > i:
          if isinstance(args[i], type_):
            initValues[key] = args[i]
          else:
            e = typeMsg(key, args[i], type_)
            raise TypeError(e)

      #  Retrieves values from keyword arguments
      for (key, type_) in valTypes.items():
        if key in kwargs:
          val = kwargs[key]
          if isinstance(val, type_):
            initValues[key] = val
          else:
            e = typeMsg(key, val, type_)
            raise TypeError(e)

      #  Creates default values for missing arguments
      for (key, defVal) in defVals.items():
        if key not in initValues:
          initValues[key] = defVal(self)

      #  Assigns values
      for (key, value) in initValues.items():
        if value is None:
          setattr(self, key, value)

    return __init__

  @staticmethod
  def _slotsFactory(boxes: list[tuple[str, AttriBox]]) -> list[str]:
    """This factory creates the '__slots__' list which is used to restrict
    the namespace to the AttriBox instances."""
    return [box[0] for box in boxes]

  def compile(self) -> dict:
    """The namespace created by the BaseNamespace class is updated with
    the '__init__' function created by the factory function."""
    namespace = OverloadSpace.compile(self)
    oldInit = namespace.get('__init__', None)
    oldGetAttr = namespace.get('__getattr__', None)
    boxes = self._getAllBoxes()
    namespace['__field_boxes__'] = self._getFieldBoxes()
    namespace['__slots__'] = self._slotsFactory(boxes)
    if oldInit is None or oldInit is object.__init__:
      newInit = self._initFactory(boxes)
      namespace['__init__'] = newInit
    if oldGetAttr is None:
      newGetAttr = self._getattrFactory(boxes)
      namespace['__getattr__'] = newGetAttr
    return namespace
