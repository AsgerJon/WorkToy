"""EZNameSpace provides the namespace object for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AttriBox, ExplicitBox
from worktoy.base import LoadSpace
from worktoy.static import OverloadEntry, typeCast, maybe
from worktoy.mcls import CallMeMaybe
from worktoy.text import typeMsg
from worktoy.waitaminute import ArgumentException

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  BoxDict = dict[str, AttriBox]
  BoxList = list[AttriBox]
  BoxKeys = list[str]
  DefGetters = dict[str, CallMeMaybe]
else:
  BoxDict = object
  BoxList = object
  BoxKeys = object
  DefGetters = object


class EZSpace(LoadSpace):
  """EZNameSpace provides the namespace object for the EZData class."""

  __field_boxes__ = None

  def _getFieldBoxDict(self) -> BoxDict:
    """This method returns the field boxes."""
    bases = [*self.getBaseClasses(), self]
    boxes = {}
    for base in bases:
      baseBoxes = maybe(getattr(base, '__field_boxes__', None), {})
      boxes = {**boxes, **baseBoxes}
    return boxes

  def _addFieldBox(self, key: str, box: AttriBox) -> None:
    """This method adds a field box to the namespace."""
    boxes = self._getFieldBoxDict()
    self.__field_boxes__ = {**boxes, key: box}

  def _getFieldBoxKeys(self) -> BoxKeys:
    """This method returns the keys of the field boxes."""
    return [key for (key, box) in self._getFieldBoxDict().items()]

  def _getFieldBoxes(self, ) -> BoxList:
    """This method returns the field boxes."""
    return [box for (key, box) in self._getFieldBoxDict().items()]

  def _getFieldBoxDefGetters(self, ) -> DefGetters:
    """This method returns the default getters for the field boxes."""
    out = {}
    boxDict = self._getFieldBoxDict()
    for (key, box) in boxDict.items():
      out[key] = box.getDefaultFactory()
    return out

  def __setitem__(self, key: str, value: object) -> None:
    """This method sets the key, value pair in the namespace."""
    if isinstance(value, AttriBox):
      return self._addFieldBox(key, value)
    if isinstance(value, (OverloadEntry, CallMeMaybe)):
      return LoadSpace.__setitem__(self, key, value)
    if self.isSpecialKey(key):
      return dict.__setitem__(self, key, value)
    box = ExplicitBox(value)
    self._addFieldBox(key, box)

  def _getattrFactory(self, ) -> CallMeMaybe:
    """This factory creates the '__getattr__' method for the class."""
    defGetters = self._getFieldBoxDefGetters()

    def __getattr__(instance: object, key: str) -> object:
      """This automatically generated '__getattr__' method retrieves the
      AttriBox instances."""
      if key in defGetters:
        setattr(instance, key, defGetters[key](instance))
      return object.__getattribute__(instance, key)

    return __getattr__

  def _initFactory(self) -> CallMeMaybe:
    """This factory creates the '__init__' method for the class."""

    boxList = self._getFieldBoxes()
    boxDict = self._getFieldBoxDict()
    keys = self._getFieldBoxKeys()
    boxTypes = [box.getFieldClass() for box in boxList]
    defGetters = self._getFieldBoxDefGetters()

    def __init__(instance: object, *args, **kwargs) -> None:
      """This automatically generated '__init__' method populates the
      AttriBox instances."""
      initValues = dict()
      clsName = self.__class__.__name__
      nArgs = len(args)
      nKeys = len(keys)

      if nArgs > nKeys:
        fName = '%s.__init__' % clsName
        raise ArgumentException(fName, nArgs, 0, nKeys)

      for (i, (key, box)) in enumerate(boxDict.items()):
        if i < nArgs:
          castArg = typeCast(args[i], box.getFieldClass())
          initValues[key] = castArg

      for (key, type_) in boxDict.items():
        if key in kwargs:
          castArg = typeCast(kwargs[key], type_)
          initValues[key] = castArg

      for (key, box) in boxDict.items():
        if key not in initValues:
          if isinstance(box, ExplicitBox):
            if box.hasExplicitDefault():
              val = box.getExplicitDefault()
            else:
              val = box.getFieldClass()()
          elif isinstance(box, AttriBox):
            val = box.getDefaultFactory()(instance)
          else:
            e = typeMsg('box', box, AttriBox)
            raise TypeError(e)
          initValues[key] = val

      for (key, value) in initValues.items():
        setattr(instance, key, value)

    return __init__

  def compile(self, ) -> dict:
    """Compile the namespace."""
    out = LoadSpace.compile(self)
    out['__field_boxes__'] = self._getFieldBoxDict()
    out['__getattr__'] = self._getattrFactory()
    if '__init__' not in out.get('__overload_entries__', {}):
      out['__init__'] = self._initFactory()
    return out
