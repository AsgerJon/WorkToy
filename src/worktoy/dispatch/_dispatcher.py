"""
Dispatcher encapsulates the mapping from type signature to function
objects and thus provides the core overloading functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..core.sentinels import THIS, FALLBACK, WILDCARD
from ..utilities import maybe
from ..waitaminute.dispatch import DispatchException, CastMismatch, \
  HashMismatch
from . import TypeSignature

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, Optional, TypeAlias, Self

  FuncObject: TypeAlias = Callable[..., Any]
  SigFuncMap: TypeAlias = Dict[TypeSignature, FuncObject]
  SigFuncList: TypeAlias = list[tuple[TypeSignature, FuncObject]]


class Dispatcher(Object):
  """
  Dispatcher encapsulates the mapping from type signature to function
  objects and thus provides the core overloading functionality.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __sig_funcs__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _sortSigFuncs(sigFuncs: SigFuncList) -> SigFuncList:
    out = sorted(sigFuncs, key=lambda x: x[0].mroLen(), reverse=True)
    out = sorted(out, key=lambda x: int(FALLBACK in x[0]), )
    return sorted(out, key=lambda x: int(WILDCARD in x[0]), )

  def _getSigFuncList(self, ) -> SigFuncList:
    noTHIS = []
    for sig, func in self.__sig_funcs__:
      if THIS in sig:
        continue
      noTHIS.append((sig, func,))
    return self._sortSigFuncs(noTHIS, )

  def _getSigFuncMap(self, ) -> SigFuncMap:
    return {k: v for k, v in self._getSigFuncList()}

  def _getFallbackFunction(self, ) -> Callable:
    for sig, func in self.__sig_funcs__:
      if FALLBACK in sig:
        return func
    raise ValueError(FALLBACK)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, sigFuncs: Optional[SigFuncList] = None) -> None:
    if isinstance(sigFuncs, dict):
      sigFuncs = [(sig, func,) for sig, func in sigFuncs.items()]
    self.__sig_funcs__ = maybe(sigFuncs, [], )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self

    def wrap(*args, **kwargs) -> Any:
      return self(instance, *args, **kwargs)

    return wrap

  def __call__(self, instance: Any, *args: Any, **kwargs: Any) -> Any:
    #  FAST
    argSig = TypeSignature.fromArgs(*args, )
    hashFunc = dict.get(self._getSigFuncMap(), argSig, None)
    # if hashFunc is not None:
    #   return hashFunc(instance, *args, **kwargs)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  SLOW
    slowArgs = []
    sigFuncs = self._getSigFuncList()
    posArgs = None
    for sig, func in sigFuncs:
      try:
        posArgs = sig.fast(*args)
      except HashMismatch:
        pass
      else:
        return func(instance, *args, **kwargs)
    for sig, func in self._getSigFuncList():
      try:
        castArgs = sig.cast(*args, )
      except CastMismatch:
        continue
      else:
        return func(instance, *castArgs, **kwargs)
    else:
      try:
        fallbackFunc = self._getFallbackFunction()
      except ValueError as valueError:
        raise DispatchException(self, args, (valueError,))
      return fallbackFunc(instance, *args, **kwargs)

  def __set_name__(self, owner: type, name: str) -> None:
    """
    Set the name of the dispatcher in the owner class.
    This is called when the dispatcher is assigned to a class variable.
    """
    self.copyTypes(THIS, owner, )
    oldOwner = self.getFieldOwner()
    if oldOwner is not None:
      self.copyTypes(oldOwner, owner, )
    return Object.__set_name__(self, owner, name)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def copyTypes(self, *types: type) -> None:
    oldSigFuncs = self.__sig_funcs__
    newSigFuncs = []
    for sig, func in oldSigFuncs:
      newSig = sig.swapType(*types, )
      newSigFuncs.append((newSig, func,))
      if newSig == sig:
        continue
      newSigFuncs.append((sig, func,))
    self.__sig_funcs__ = self._sortSigFuncs(newSigFuncs)

  def overload(self, *types) -> Callable[[FuncObject], Self]:
    def decorator(func: FuncObject) -> Self:
      sig = TypeSignature(*types, )
      self.__sig_funcs__.append((sig, func,))
      return self

    return decorator

  def clone(self, ) -> Self:
    """
    Clone the dispatcher, creating a new instance with the same type
    signatures, functions, field name and field owner.
    """
    cls = type(self)
    out = cls([*self._getSigFuncList(), ])
    owner, name = self.getFieldOwner(), self.getFieldName()
    out.__set_name__(owner, name)
    return out
