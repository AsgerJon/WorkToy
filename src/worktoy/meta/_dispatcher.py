"""Dispatcher is a callable class that passes the call to the given
overload that matches the type signature of the arguments received. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe
from worktoy.meta import Overload, TypeSig, DispatchException
from worktoy.text import typeMsg, monoSpace

try:
  from typing import TYPE_CHECKING, Any, Callable
except ImportError:
  TYPE_CHECKING = False
  Any = object
  Callable = object
if TYPE_CHECKING:
  OverloadList = list[Overload]
  SigMap = dict[TypeSig, Overload]
  TypeSigList = list[TypeSig]
else:
  OverloadList = object
  SigMap = object
  TypeSigList = object


class _DispatchCall:
  """This class encapsulates the callable created by the dispatcher. """

  __func__ = None
  __self__ = None
  __name__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the dispatch call. """
    self.__name__, self.__func__, self.__self__ = [*args, None][:3]

  def __call__(self, *args, **kwargs) -> Any:
    """Calls the function with the given arguments. """
    if self.__self__ is None:
      return self.__func__(*args, **kwargs)
    return self.__func__(self.__self__, *args, **kwargs)


class Dispatcher:
  """Dispatcher is a callable class that passes the call to the given
  overload that matches the type signature of the arguments received. """

  __field_metaclass__ = None
  __field_key__ = None
  __field_name__ = None
  __field_owner__ = None
  __overload_entries__ = None
  __sig_map__ = None
  __class_method_flag__ = None

  def setFieldMetaclass(self, mcls: type) -> None:
    """Sets the field metaclass. """
    if not isinstance(mcls, type):
      e = typeMsg('mcls', mcls, type)
      raise TypeError(e)
    self.__field_metaclass__ = mcls

  def getFieldMetaclass(self, ) -> type:
    """Returns the field metaclass. """
    if self.__field_metaclass__ is None:
      e = """The field metaclass is not set."""
      raise TypeError(e)
    return self.__field_metaclass__

  def setFieldKey(self, fieldKey: str) -> None:
    """Sets the field key. """
    if not isinstance(fieldKey, str):
      e = typeMsg('fieldKey', fieldKey, str)
      raise TypeError(e)
    self.__field_key__ = fieldKey

  def getFieldKey(self, ) -> str:
    """Returns the field key. """
    if self.__field_key__ is None:
      e = """The field key is not set."""
      raise TypeError(e)
    return self.__field_key__

  def setFieldName(self, fieldName: str) -> None:
    """Sets the field name. """
    if not isinstance(fieldName, str):
      e = typeMsg('fieldName', fieldName, str)
      raise TypeError(e)
    self.__field_name__ = fieldName

  def getFieldName(self, ) -> str:
    """Returns the field name. """
    if self.__field_name__ is None:
      e = """The field name is not set."""
      raise TypeError(e)
    return self.__field_name__

  def setFieldOwner(self, fieldOwner: type) -> None:
    """Sets the field owner. """
    mcls = self.getFieldMetaclass()
    if not isinstance(fieldOwner, mcls):
      e = typeMsg('fieldOwner', fieldOwner, mcls)
      raise TypeError(e)
    self.__field_owner__ = fieldOwner

  def getFieldOwner(self, ) -> type:
    """Returns the field owner. """
    if self.__field_owner__ is None:
      e = """The field owner is not set."""
      raise TypeError(e)
    return self.__field_owner__

  def getOverloads(self, ) -> OverloadList:
    """Returns the overload entries. """
    return maybe(self.__overload_entries__, [])

  def getMappings(self, ) -> SigMap:
    """Returns the mappings. """
    if self.__sig_map__ is None:
      e = """The mappings are not set."""
      raise TypeError(e)
    return self.__sig_map__

  #  Main methods

  def getTypeSignatures(self, ) -> TypeSigList:
    """Returns the type signatures of the dispatcher. """
    out = []
    for (sig, fun) in self.getMappings().items():
      out.append(sig)
    return out

  def addOverload(self, overloadEntry: Overload) -> None:
    """Adds an overload entry to the dispatcher. """
    existing = self.getOverloads()
    self.__overload_entries__ = [*existing, overloadEntry]

  def updateMappings(self, ) -> None:
    """Updates the mappings from the new overload settings. """
    cls = self.getFieldOwner()
    mcls = self.getFieldMetaclass()
    self.__sig_map__ = {}
    for entry in self.getOverloads():
      rawSig = entry.getTypeSignature()
      types = []
      for type_ in rawSig:
        if getattr(type_, '__THIS_ZEROTON__', None) is not None:
          types.append(cls)
        elif getattr(type_, '__TYPE_ZEROTON__', None) is not None:
          types.append(mcls)
        elif isinstance(type_, type):
          types.append(type_)
        else:
          e = typeMsg('type', type_, type)
          raise TypeError(e)
      sig = TypeSig(*types, )
      self.__sig_map__[sig] = entry.getWrappedFunction()

  def hereIsMyNumber(self, instance: object) -> Callable:
    """Creates the callable bound to the instance. """

    def callMeMaybe(*args, **kwargs) -> None:
      for (sig, fun) in self.getMappings().items():
        castArg = sig.fastCast(*args, )
        if castArg is None:
          continue
        if instance is None:
          return fun(*args, **kwargs)
        return fun(instance, *args, **kwargs)
      for (sig, fun) in self.getMappings().items():
        castArg = sig.cast(*args, )
        if castArg is None:
          continue
        if instance is None:
          return fun(*args, **kwargs)
        return fun(instance, *args, **kwargs)
      raise DispatchException(self, *args)

    return callMeMaybe

  def __get__(self, instance: object, owner: type) -> Any:
    """Descriptor method for the dispatcher. """
    if instance is None:
      return self
    return self.hereIsMyNumber(instance)

  def __set_name__(self, owner: type, name: str) -> None:
    """This method is invoked when the owning class is created. """
    mcls = self.getFieldMetaclass()
    key = self.getFieldKey()
    if not isinstance(owner, mcls):
      e = """The owner is not derived from the set metaclass!"""
      raise TypeError(e)
    if key != name:
      e = """The key: '%s' does not match the name: '%s'!"""
      raise ValueError(e % (key, name))
    self.setFieldName(name)
    self.setFieldOwner(owner)
    self.updateMappings()

  def __init__(self, fieldMetaclass: type, key: str, **kwargs) -> None:
    """Initializes the dispatcher. """
    self.setFieldMetaclass(fieldMetaclass)
    self.setFieldKey(key)
