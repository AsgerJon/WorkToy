"""
BaseSpace provides the namespace class used by worktoy.mcls.BaseMeta
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from ..core.sentinels import WILDCARD
from ..utilities import maybe
from ..waitaminute import VariableNotNone
from ..static import TypeSig
from . import AbstractNamespace
from .space_hooks import OverloadSpaceHook, PreClassSpaceHook, LoadSpaceHook
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Callable, Any

  OverloadMap: TypeAlias = dict[str, dict[TypeSig, Callable[..., Any]]]
  Bases: TypeAlias = tuple[type, ...]


class BaseSpace(AbstractNamespace):
  """
  BaseSpace is the namespace used by BaseMeta. It enables function
  overloading and related features via hook registration.

  Classes defined using this namespace support method overloading through
  hooks installed automatically in the class body. These hooks handle
  overload collection, dispatch construction, and support for 'THIS' as a
  placeholder during class creation.

  The overload mechanism and other behavior are defined in
  `worktoy.mcls.hooks`. This namespace is returned from BaseMeta.__prepare__.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __overload_map__ = None

  #  Public Variables
  loadSpaceHook = LoadSpaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: type, name: str, bases: Bases, **kw) -> None:
    AbstractNamespace.__init__(self, mcls, name, bases, **kw)
    self.__overload_map__ = dict()
    for space in self.getMRONamespaces():
      for name, sigFunc in getattr(space, '__overload_map__', {}).items():
        if name not in self.__overload_map__:
          self.__overload_map__[name] = dict()
        for sig, func in sigFunc.items():
          if sig not in self.__overload_map__[name]:
            self.__overload_map__[name][sig] = func

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addOverload(self, name: str, sig: TypeSig, func: Callable) -> None:
    if self.__overload_map__ is None:
      self.__overload_map__ = dict()
    if name not in self.__overload_map__:
      self.__overload_map__[name] = dict()
    self.__overload_map__[name][sig] = func

  def addOverloads(self, *loads: tuple[str, TypeSig, Callable]) -> None:
    """
    Adds multiple overloads to the namespace.
    Each overload is a dictionary mapping TypeSig to Callable.
    """
    for load in loads:
      self.addOverload(*load, )

  def getOverloads(self, ) -> OverloadMap:
    return maybe(self.__overload_map__, {})
