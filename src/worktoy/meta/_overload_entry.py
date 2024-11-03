"""OverloadEntry marks a type signature to function mapping used whne
creating overloaded classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import TypeSig
from worktoy.text import typeMsg, monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Any, Callable
except ImportError:
  Callable = object
  Any = object

from worktoy.parse import maybe

if TYPE_CHECKING:
  TypeSigs = list[TypeSig]
  TypeList = list[type]
else:
  TypeSigs = object
  TypeList = object


class OverloadEntry:
  """OverloadEntry marks a type signature to function mapping used whne
  creating overloaded classes. """

  #  Private variables
  __space_key__ = None
  __field_name__ = None
  __field_owner__ = None
  __field_metaclass__ = None
  __raw_types__ = None
  __decorated_function__ = None
  __type_sig__ = None
  __type_list__ = None

  #  Trivial accessor functions

  def getSpaceKey(self, ) -> str:
    """Getter-function for the space key."""
    if self.__space_key__ is None:
      e = """The space key is not set."""
      raise TypeError(e)
    if isinstance(self.__space_key__, str):
      return self.__space_key__
    e = typeMsg('__space_key__', self.__space_key__, str)
    raise TypeError(e)

  def setSpaceKey(self, spaceKey: str) -> None:
    """Setter-function for the space key."""
    if not isinstance(spaceKey, str):
      e = typeMsg('spaceKey', spaceKey, str)
      raise TypeError(e)
    self.__space_key__ = spaceKey

  def setMetaclass(self, mcls: type) -> None:
    """Setter-function for the metaclass creating the class"""
    if not isinstance(mcls, type):
      e = typeMsg('mcls', mcls, type)
      raise TypeError(e)
    self.__field_metaclass__ = mcls

  def getMetaclass(self) -> type:
    """Getter-function for the metaclass creating the class"""
    if self.__field_metaclass__ is None:
      e = """The metaclass is not set."""
      raise TypeError(e)
    if isinstance(self.__field_metaclass__, type):
      if issubclass(self.__field_metaclass__, type):
        return self.__field_metaclass__
    e = typeMsg('__field_metaclass__', self.__field_metaclass__, type)
    raise TypeError(e)

  def setFieldName(self, fieldName: str) -> None:
    """Setter-function for the field name."""
    if not isinstance(fieldName, str):
      e = typeMsg('fieldName', fieldName, str)
      raise TypeError(e)
    self.__field_name__ = fieldName

  def getFieldName(self, ) -> str:
    """Getter-function for the field name."""
    if self.__field_name__ is None:
      e = """The field name is not set."""
      raise TypeError(e)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(e)

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Setter-function for the field owner."""
    if not isinstance(fieldOwner, type):
      e = typeMsg('fieldOwner', fieldOwner, type)
      raise TypeError(e)
    self.__field_owner__ = fieldOwner

  def getFieldOwner(self, ) -> type:
    """Getter-function for the field owner."""
    if self.__field_owner__ is None:
      e = """The field owner is not set."""
      raise TypeError(e)
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(e)

  def setRawTypes(self, *types: type) -> None:
    """Setter-function for the raw types."""
    if self.__raw_types__ is not None:
      e = """The raw types are already set."""
      raise TypeError(e)
    self.__raw_types__ = [*types, ]

  def getRawTypes(self, ) -> TypeList:
    """Getter-function for the raw types"""
    if self.__raw_types__ is None:
      e = """The raw types are not set."""
      raise TypeError(e)
    return self.__raw_types__

  def setDecoratedFunction(self, decoratedFunction: Callable) -> None:
    """Setter-function for the decorated function."""
    if self.__decorated_function__ is not None:
      e = """The decorated function is already set."""
      raise TypeError(e)
    if not callable(decoratedFunction):
      e = typeMsg('decoratedFunction', decoratedFunction, Callable)
      raise TypeError(e)
    self.__decorated_function__ = decoratedFunction

  def getDecoratedFunction(self, ) -> Callable:
    """Getter-function for the decorated function."""
    if self.__decorated_function__ is None:
      e = """The decorated function is not set."""
      raise TypeError(e)
    if not callable(self.__decorated_function__):
      e = typeMsg('__decorated_function__',
                  self.__decorated_function__,
                  Callable)
      raise TypeError(e)
    return self.__decorated_function__

  def getTypeSig(self, ) -> TypeSig:
    """Getter-function for the type signature."""
    if self.__type_sig__ is None:
      e = """The type signatures are not set."""
      raise TypeError(e)
    return self.__type_sig__

  # Special accessor functions

  def _createTypeSig(self, ) -> None:
    """This method is invoked when the owning class is created. """
    rawTypes = self.getRawTypes()
    cls = self.getFieldOwner()
    mcls = self.getMetaclass()
    readyTypes = []
    for rawType in rawTypes:
      if getattr(rawType, '__THIS_ZEROTON__', None) is not None:
        readyTypes.append(cls)
      elif getattr(rawType, '__TYPE_ZEROTON__', None) is not None:
        readyTypes.append(mcls)
      elif isinstance(rawType, type):
        readyTypes.append(rawType)
      else:
        e = typeMsg('rawType', rawType, type)
        raise TypeError(e)
    self.__type_sig__ = TypeSig(*readyTypes)

  def __init__(self, *types) -> None:
    """Initialize the OverloadEntry object."""
    self.setRawTypes(*types)

  def __set_name__(self, owner: type, name: str) -> None:
    """This method is invoked when the owning class is created. """
    mcls = self.getMetaclass()
    if not isinstance(owner, mcls):
      e = """The owner is not derived from the set metaclass!"""
      raise TypeError(monoSpace(e))
    self.setFieldName(name)
    self.setFieldOwner(owner)
    self._createTypeSig()
