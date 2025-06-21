"""EZHook collects the field entries in EZData class bodies. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType

from ..mcls.hooks import AbstractHook
from ..text import stringList
from ..waitaminute import attributeErrorFactory, ReservedName

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Iterator
  from worktoy.ezdata import EZData


class EZHook(AbstractHook):
  """EZHook collects the field entries in EZData class bodies. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __reserved_names__ = """__slots__, __init__, __eq__, __str__, __repr__,
    __iter__, __getitem__, __setitem__, __getattr__"""
  __ignore_names__ = """__module__, __dict__, __weakref__, __class__, 
  __qualname__, __firstlineno__, __doc__, __static_attributes__, 
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @classmethod
  def _getReservedNames(cls) -> list[str]:
    """Get the reserved names for the EZData class."""
    return stringList(cls.__reserved_names__)

  @classmethod
  def _getIgnoreNames(cls) -> list[str]:
    """Get the ignore names for the EZData class."""
    return stringList(cls.__ignore_names__)

  @classmethod
  def validateName(cls, name: str, ) -> None:
    """
    Raises ReservedName if the name is one of the reserved names.
    """
    if name in cls._getReservedNames():
      raise ReservedName(name)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Hook methods

  def preCompileHook(self, compiledSpace: dict) -> dict:
    """The preCompileHook method is called before the class is compiled."""
    dataFields = self.space.getDataFields()
    compiledSpace['__slots__'] = (
        *[dataField.key for dataField in dataFields],)
    return compiledSpace

  def postCompileHook(self, compiledSpace: dict) -> dict:
    """The postCompileHook method is called after the class is compiled."""
    dataFields = self.space.getDataFields()
    initMethod = self.initFactory(*dataFields)
    eqMethod = self.eqFactory(*dataFields)
    strMethod = self.strFactory(*dataFields)
    reprMethod = self.reprFactory(*dataFields)
    iterMethod = self.iterFactory(*dataFields)
    getItemMethod = self.getItemFactory(*dataFields)
    setItemMethod = self.setItemFactory(*dataFields)
    getAttrMethod = self.getAttrFactory(*dataFields)
    compiledSpace['__init__'] = initMethod
    compiledSpace['__eq__'] = eqMethod
    compiledSpace['__str__'] = strMethod
    compiledSpace['__repr__'] = reprMethod
    compiledSpace['__iter__'] = iterMethod
    compiledSpace['__getitem__'] = getItemMethod
    compiledSpace['__setitem__'] = setItemMethod
    compiledSpace['__getattr__'] = getAttrMethod
    return compiledSpace

  def setItemHook(self, key: str, value: Any, oldValue: Any, ) -> bool:
    """The setItemHook method is called when an item is set in the
    enumeration."""
    if key in self._getIgnoreNames():
      return False
    if key in self._getReservedNames():
      if hasattr(value, '__is_root__'):
        return False
      raise ReservedName(key)
    if callable(value):
      return False
    self.space.addField(key, type(value), value)
    return True

  # \_____________________________________________________________________/ #
  #  Method factories
  # /¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\ #
  @staticmethod
  def initFactory(*dataFields) -> FunctionType:
    """
    Creates the '__init__' method for the EZData class.
    """

    slotKeys = [dataField.key for dataField in dataFields]
    defVals = [dataField.val for dataField in dataFields]

    def __init__(self, *args, **kwargs):
      """
      The generated '__init__' method sets attributes on the instance
      based on given arguments. Keyword arguments take precedence.
      Positional arguments are applied in order.
      """
      posArgs = [*args, ]
      while len(posArgs) < len(slotKeys):
        posArgs.append(None)
      for key, defVal in zip(slotKeys, defVals):
        setattr(self, key, defVal)
      for key, arg in zip(slotKeys, posArgs):
        if arg is not None:
          setattr(self, key, arg)
      for key in slotKeys:
        if key in kwargs:
          setattr(self, key, kwargs[key])

    return __init__

  @staticmethod
  def eqFactory(*dataFields) -> FunctionType:
    """
    Creates the '__eq__' method for the EZData class.
    """

    def __eq__(self, other: EZData) -> bool:
      """
      Instances of EZData are equal if each of their data fields are equal.
      """
      for dataField in dataFields:
        key = dataField.key
        if getattr(self, key) != getattr(other, key):
          return False
      return True

    return __eq__

  @staticmethod
  def strFactory(*dataFields) -> FunctionType:
    """The strFactory method is called when the class is created."""

    def __str__(self) -> str:
      """The __str__ method is called when the class is created."""
      clsName = type(self).__name__
      keys = [dataField.key for dataField in dataFields]
      vals = [str(getattr(self, key)) for key in keys]
      keyVals = ['%s=%s' % (key, val) for key, val in zip(keys, vals)]
      return """%s(%s)""" % (clsName, ', '.join(keyVals))

    return __str__

  @staticmethod
  def reprFactory(*dataFields) -> FunctionType:
    """The reprFactory method is called when the class is created."""

    def __repr__(self) -> str:
      """The __repr__ method is called when the class is created."""
      clsName = type(self).__name__
      keys = [dataField.key for dataField in dataFields]
      vals = [str(getattr(self, key)) for key in keys]
      return """%s(%s)""" % (clsName, ', '.join(vals))

    return __repr__

  @staticmethod
  def iterFactory(*dataFields) -> FunctionType:
    """The iterFactory method is called when the class is created."""

    def __iter__(self, ) -> Iterator:
      """
      Implementation of the iteration protocol
      """
      for key in self.__slots__:
        yield getattr(self, key)

    return __iter__

  @staticmethod
  def getItemFactory(*dataFields) -> FunctionType:
    """The getItemFactory method is called when the class is created."""

    def __getitem__(self, key: str) -> object:
      """The __getitem__ method is called when the class is created."""
      if key in self.__slots__:
        return getattr(self, key)
      raise KeyError(key)

    return __getitem__

  @staticmethod
  def setItemFactory(*dataFields) -> FunctionType:
    """The setItemFactory method is called when the class is created."""

    def __setitem__(self, key: str, value: object) -> None:
      """The __setitem__ method is called when the class is created."""
      if key in self.__slots__:
        return setattr(self, key, value)
      raise KeyError(key)

    return __setitem__

  @staticmethod
  def getAttrFactory(*dataFields) -> FunctionType:
    """The getAttrFactory method is called when the class is created."""

    def __getattr__(self, key: str) -> Any:
      """The __getattr__ method is called when the class is created."""
      if key in self.__slots__:
        return getattr(self, key)
      raise attributeErrorFactory(type(self), key)

    return __getattr__
