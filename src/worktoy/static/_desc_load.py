"""
DescLoad provides inline function overloading not relying on the owning
class deriving from a specific metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field
from ..core import Object
from . import TypeSig, Dispatch
from ..utilities import maybe
from ..waitaminute import attributeErrorFactory

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, Self, Type, Any, Iterator


class TempLoad(Object):
  """Created by each load call. The __set_name__ then creates entry in
  DescLoad registry for the owner. In this registry, we create registry on
  the name of the function. This registry maps from type signature to
  function body. """


class DescLoad(Object):
  """
  DescLoad provides inline function overloading not relying on the owning
  class deriving from a specific metaclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __desc_loads__ = None

  #  Private Variables
  __field_function__ = None
  __type_sigs__ = None

  #  Public Variables
  func = Field()
  sigs = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def getDescLoads(cls) -> list[Self]:
    return maybe(cls.__desc_loads__, [])

  @func.GET
  def _getFunc(self) -> Callable:
    return self.__field_function__

  @sigs.GET
  def _getSigs(self) -> list[TypeSig]:
    return self.__type_sigs__

  def _generateName(self, ) -> str:
    """
    Generates a name for the dispatch object at the given name,
    """
    infoSpec = """__%s_dispatcher__"""
    return infoSpec % self.__field_name__

  def getRelatedEntries(self) -> list[Self]:
    """Returns the contents of the DescLoad registry filtered to those
    having same name as self. To avoid leakage, these must be removed from
    the registry upon creation of the dispatcher. """
    name = self.__field_function__.__name__
    out = []
    for item in self.getDescLoads():
      if item.__field_function__.__name__ == name:
        out.append(item)
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addSig(self, sig: TypeSig) -> None:
    """Adds a type signature to the DescLoad object. """
    existing = self.sigs
    self.__type_sigs__ = [*existing, sig, ]

  def _extendSigs(self, *sigs: TypeSig) -> None:
    """Extends the type signatures of the DescLoad object with the given
    type signatures. """
    for sig in sigs:
      self._addSig(sig)

  @classmethod
  def _registerSelf(cls, self, ) -> None:
    existing = cls.getDescLoads()
    cls.__desc_loads__ = [*existing, self, ]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *types: type) -> None:
    self.__type_sigs__ = [TypeSig(*types), ]
    self._registerSelf(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, func: Callable) -> Self:
    """
    Decorator to register a function with the DescLoad descriptor.
    The function must have a type signature matching the descriptor's
    type signature.
    """
    cls = type(self)
    if isinstance(func, cls):
      # If func is already a DescLoad, extend the signatures
      self._extendSigs(*func.sigs)
      func = func.__field_function__
    self.__field_function__ = func
    return self

  def __set_name__(self, owner: Type[Object], name: str) -> None:
    """
    Only the final DescLoad object receives the __set_name__ call,
    so it builds everything from the registry.
    """
    Object.__set_name__(self, owner, name)
    pvtName = self._generateName()
    callMap = dict()
    for sig in self.__type_sigs__:
      callMap[sig] = self.__field_function__
    dispatcher = Dispatch(callMap, )
    Dispatch.__set_name__(dispatcher, owner, pvtName)
    setattr(owner, pvtName, dispatcher)

  def __get__(self, instance: Object, owner: Type[Object]) -> Any:
    if instance is None:
      return self
    pvtName = self._generateName()
    return getattr(instance, pvtName, )

  def __getattr__(self, key: str, ) -> Any:
    if key == '__name__':
      out = object.__getattribute__(self, '__field_function__').__name__
      return out
    raise attributeErrorFactory(self, key)

  def __iter__(self, ) -> Iterator[tuple[str, TypeSig, Callable]]:
    """
    Iterates over the type signatures and functions in the DescLoad object.
    """
    func = self.__field_function__
    name = func.__name__
    for sig in self.__type_sigs__:
      yield name, sig, func
