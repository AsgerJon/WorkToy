#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
"""Dispatch is a special descriptor class responsible for passing
arguments to the appropriate overloaded function. Each instance should
handle all the functions at a single name. To ensure support for THIS and
TYPE from the 'worktoy.desc' module, the Dispatch instance must be aware
of the owning class and metaclass. Since the namespace object creates the
Dispatch instances, it provides the metaclass, but cannot provide the
class, as it is not yet created. The namespace object is aware of the
metaclass and the name of the class under creation, but not the class
itself. Fortunately, the __set_name__ method is called when the descriptor
is assigned to a class. This allows the Dispatch instance to be notified
of the class the moment it is created. """
from __future__ import annotations

from worktoy.meta import OverloadEntry, TypeSig, DispatchException
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace

try:
  from typing import TYPE_CHECKING, Callable, Any
except ImportError:
  TYPE_CHECKING = False
  Callable = object
  Any = object

if TYPE_CHECKING:
  TypeSigMapping = list[tuple[TypeSig, Callable]]
else:
  TypeSigMapping = object


class Dispatch:
  """Dispatch is a special descriptor class responsible for passing
  arguments to the appropriate overloaded function. Each instance should
  handle all the functions at a single name. """

  __field_name__ = None
  __field_owner__ = None
  __field_metaclass__ = None
  __func_name__ = None
  __overload_entries__ = None
  __type_sig_mapping__ = None
  __static_method__ = None
  __class_method__ = None
  __bound_self__ = None

  def setFuncName(self, name: str) -> None:
    """Set the function name."""
    if self.__func_name__ is not None:
      e = """The function name is already set."""
      raise TypeError(e)
    if not isinstance(name, str):
      e = typeMsg('name', name, str)
      raise TypeError(e)
    self.__func_name__ = name

  def getFuncName(self) -> str:
    """Return the function name."""
    if self.__func_name__ is None:
      e = """The function name is not set."""
      raise TypeError(e)
    if isinstance(self.__func_name__, str):
      return self.__func_name__
    e = typeMsg('__func_name__', self.__func_name__, str)
    raise TypeError(e)

  def getFieldOwner(self, ) -> object:
    """Return the field owner."""
    if self.__field_owner__ is None:
      e = """The field owner is not set."""
      raise TypeError(e)
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(e)

  def getFieldMetaclass(self, ) -> type:
    """Return the field metaclass."""
    if self.__field_metaclass__ is None:
      e = """The field metaclass is not set."""
      raise TypeError(e)
    if isinstance(self.__field_metaclass__, type):
      return self.__field_metaclass__
    e = typeMsg('__field_metaclass__', self.__field_metaclass__, type)
    raise TypeError(e)

  def getFieldName(self, ) -> str:
    """Return the field name."""
    if self.__field_name__ is None:
      e = """The field name is not set."""
      raise TypeError(e)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError

  def getOverloadEntries(self, ) -> list[OverloadEntry]:
    """Return the overload entries."""
    return maybe(self.__overload_entries__, [])

  def addOverloadEntry(self, overloadEntry: OverloadEntry) -> None:
    """Add an overload entry to the dispatch."""
    if not isinstance(overloadEntry, OverloadEntry):
      e = typeMsg('overloadEntry', overloadEntry, OverloadEntry)
      raise TypeError(e)
    existing = self.getOverloadEntries()
    self.__overload_entries__ = [*existing, overloadEntry]

  def __init__(self, name: str, *overloadEntries: OverloadEntry) -> None:
    self.setFuncName(name)
    for entry in overloadEntries:
      if isinstance(entry, OverloadEntry):
        self.addOverloadEntry(entry)
      else:
        e = typeMsg('entry', entry, OverloadEntry)
        raise TypeError(e)

  def __set_name__(self, owner: object, name: str) -> None:
    """The __set_name__ method is called when the descriptor is assigned to
    a class. """
    funcName = self.getFuncName()
    if name != funcName:
      e = """Received name: '%s' not matching function name: '%s'!"""
      raise ValueError(monoSpace(e % (name, funcName)))
    self.__field_owner__ = owner
    self.__field_name__ = name
    self._buildMapping()

  def setMetaclass(self, mcls: type) -> None:
    """Set the metaclass of the class."""
    if self.__field_metaclass__ is not None:
      e = """The metaclass is already set."""
      raise TypeError(e)
    if not isinstance(mcls, type):
      e = typeMsg('mcls', mcls, type)
      raise TypeError(e)
    self.__field_metaclass__ = mcls

  def getTypeSigMapping(self, ) -> TypeSigMapping:
    """Return the type signature mapping."""
    return maybe(self.__type_sig_mapping__, [])

  def addTypeSigMapping(self,
                        typeSig: TypeSig,
                        callMeMaybe: Callable, ) -> None:
    """Add a type signature mapping."""
    if not isinstance(typeSig, TypeSig):
      e = typeMsg('typeSig', typeSig, TypeSig)
      raise TypeError(e)
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    existing = self.getTypeSigMapping()
    self.__type_sig_mapping__ = [*existing, (typeSig, callMeMaybe)]

  def getTypeSignatures(self, ) -> list[TypeSig]:
    """Return the type signatures."""
    out = []
    for (typeSig, _) in self.getTypeSigMapping():
      out.append(typeSig)
    return out

  def _buildMapping(self, ) -> None:
    """This method builds the mapping from type signature to function. It
    should be called by the __set_name__ to ensure that the mapping is
    created only after the owning class is created. """
    mcls = self.getFieldMetaclass()
    cls = self.getFieldOwner()
    name = self.getFieldName()
    overloadEntries = self.getOverloadEntries()
    static = None
    class_ = None
    funcName = self.getFuncName()
    for entry in overloadEntries:
      callMeMaybe = entry.getDecoratedFunction()
      if funcName != callMeMaybe.__name__:
        e = """Function name: '%s' does not match the name: '%s'!"""
        raise ValueError(monoSpace(e % (callMeMaybe.__name__, funcName)))

      if static is not None:
        if isinstance(callMeMaybe, staticmethod) != static:
          e = """Static method mismatch!"""
          raise TypeError(e)
      else:
        static = True if isinstance(callMeMaybe, staticmethod) else False
      if class_ is not None:
        if isinstance(callMeMaybe, classmethod) != class_:
          e = """Class method mismatch!"""
          raise TypeError(e)
      else:
        class_ = True if isinstance(callMeMaybe, classmethod) else False
      if static and class_:
        e = """Cannot have a method be both static and class!"""
        raise TypeError(e)
      for rawTypes in entry.getRawTypes():

        types = []
        for rawType in rawTypes:
          if getattr(rawType, '__THIS_ZEROTON__', None) is not None:
            types.append(cls)
          elif getattr(rawType, '__TYPE_ZEROTON__', None) is not None:
            types.append(mcls)
          elif isinstance(rawType, type):
            types.append(rawType)
          else:
            e = typeMsg('rawType', rawType, type)
            raise TypeError(e)
        typeSig = TypeSig(*types)

        self.addTypeSigMapping(typeSig, callMeMaybe)
    self.__static_method__ = static
    self.__class_method__ = class_

  def __call__(self, *args, **kwargs) -> object:
    """The __call__ method is called when the descriptor is called. """
    for (typeSig, callMeMaybe) in self.getTypeSigMapping():
      castArg = typeSig.fastCast(*args, )
      if castArg is None:
        continue
      __self__ = self.getSelf()
      if __self__ is None:
        return callMeMaybe(*args, **kwargs)
      return callMeMaybe(__self__, *args, **kwargs)
    for (typeSig, callMeMaybe) in self.getTypeSigMapping():
      castArg = typeSig.cast(*args, )
      if castArg is None:
        continue
      __self__ = self.getSelf()
      if __self__ is None:
        return callMeMaybe(*args, **kwargs)
      return callMeMaybe(__self__, *args, **kwargs)
    raise DispatchException(self, *args)

  def isStaticMethod(self) -> bool:
    """Return True if the method is a static method."""
    if self.__static_method__ is None:
      e = """The Dispatch instance has not been build!"""
      raise RuntimeError(e)
    return True if self.__static_method__ else False

  def isClassMethod(self) -> bool:
    """Return True if the method is a class method."""
    if self.__class_method__ is None:
      e = """The Dispatch instance has not been build!"""
      raise RuntimeError(e)
    return True if self.__class_method__ else False

  def getSelf(self, ) -> Any:
    """Getter-function for the bound object"""
    return self.__bound_self__

  def setSelf(self, obj: Any) -> None:
    """Setter-function for the bound object"""
    self.__bound_self__ = obj

  def delSelf(self, ) -> None:
    """Deleter-function for the bound object"""
    self.__bound_self__ = None

  def __get__(self, instance: object, owner: type) -> Any:
    """The __get__ method is called when the descriptor is accessed. """
    if instance is None:
      if self.isClassMethod():
        self.setSelf(owner)
      else:
        self.delSelf()
      return self
    if self.isStaticMethod():
      self.delSelf()
    else:
      self.setSelf(instance)
    return self
