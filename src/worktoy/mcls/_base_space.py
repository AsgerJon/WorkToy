"""
BaseSpace provides the namespace class used by worktoy.mcls.BaseMeta
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..dispatch import TypeSig
from ..utilities import maybe
from . import AbstractNamespace
from .space_hooks import LoadSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Callable, Any, Self

  SigFunc: TypeAlias = dict[TypeSig, Callable[..., Any]]
  OverloadMap: TypeAlias = dict[str, SigFunc]
  VariadicList: TypeAlias = list[tuple[TypeSig, Callable[..., Any]]]
  VariadicMap: TypeAlias = dict[str, VariadicList]
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
  'worktoy.mcls.space_hooks'. This namespace is returned from
  BaseMeta.__prepare__.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __overload_map__ = None
  __variadic_overload_map__ = None
  __fallback_map__ = None
  __finalizer_map__ = None

  #  Public Variables
  loadSpaceHook = LoadSpaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: type, name: str, bases: Bases, **kw) -> None:
    AbstractNamespace.__init__(self, mcls, name, bases, **kw)
    for base in bases:
      try:
        space: Self = getattr(base, '__namespace__')
      except AttributeError:
        continue
      else:
        try:
          overloadMap: OverloadMap = space.getOverloads()
        except AttributeError:
          continue
        else:
          for overloadName, sigFuncMap in {**overloadMap, }.items():
            for sig, func in {**sigFuncMap, }.items():
              self.addOverload(overloadName, sig, func)
          variadicMap: VariadicMap = space.getVariadics()
          for variadicName, variadicList in {**variadicMap, }.items():
            for sig, func in [*variadicList, ]:
              self.addVariadic(variadicName, sig, func)
          fallbackMap: dict[str, Callable] = space.getFallbacks()
          for fallbackName, func in {**fallbackMap, }.items():
            self.addFallback(fallbackName, func)
          finalizerMap: dict[str, Callable] = space.getFinalizers()
          for finalizerName, func in {**finalizerMap, }.items():
            self.addFinalizer(finalizerName, func)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addOverload(self, name: str, sig: TypeSig, func: Callable, ) -> None:
    """
    This method sets the mapping between the given type signature and
    function object to the overloaded name.

    Parameters
    ----------
    name: str
      The name of the overloaded function.
    sig: TypeSig
      The type signature for the overload.
    func: Callable
      The function object to be dispatched when given arguments matching
      the given type signature.
    """
    existing = self.getOverloads()
    if name not in existing:
      existing[name] = dict()
    existing[name][sig] = func
    self.__overload_map__ = {**existing, }

  def getOverloads(self, ) -> OverloadMap:
    """
    This method returns dictionary mapping names of overloaded function to
    the dictionary mapping type signature to function object assigned to
    the overload at the given name.

    Returns
    -------
    OverloadMap: TypeAlias = dict[str, dict[TypeSig, Callable]]
      Mapping from overloaded name to its mapping from type signature to
      function object.
    """
    return maybe(self.__overload_map__, {})

  def addVariadic(self, name: str, sig: TypeSig, func: Callable) -> None:
    """Register a variadic '(TypeSig, func)' pair under 'name'. The
    'TypeSig' must carry a trailing 'ARGS' sentinel as its last raw
    type. Stored in a list rather than a dict because 'ARGS'
    instances are not hashable and the dispatcher matches variadic
    sigs by structural iteration, not by hash lookup."""
    existing = self.getVariadics()
    if name not in existing:
      existing[name] = []
    existing[name] = [*existing[name], (sig, func,)]
    self.__variadic_overload_map__ = {**existing, }

  def getVariadics(self, ) -> VariadicMap:
    """Mapping from overloaded name to its list of variadic
    '(TypeSig, func)' pairs. Returns an empty dict when no variadic
    overloads have been registered."""
    return maybe(self.__variadic_overload_map__, {})

  def addFallback(self, name: str, func: Callable) -> None:
    """
    Sets the fallback function for the overloaded name to the given
    function object. These fallbacks are dispatched by the overload
    system when no other assigned overload matches the type signature of
    given arguments.

    Parameters
    ----------
    name: str
      The name of the overloaded function for which to set the fallback.
    func: Callable
      The function object to be dispatched when given arguments that do
      not match any of the type signatures assigned to the overload at the
      given name.
    """
    existing = self.getFallbacks()
    existing[name] = func
    self.__fallback_map__ = {**existing, }

  def getFallbacks(self) -> dict[str, Callable]:
    """
    This method returns the mappings from overloaded names to assigned
    fallback functions.

    Returns
    -------
    dict[str, Callable]
      Mapping from overloaded name to its assigned fallback function.
    """
    return maybe(self.__fallback_map__, dict())

  def addFinalizer(self, name: str, func: Callable) -> None:
    """
    Sets the finalizer function for the overloaded name to the given
    function object. Finalizer functions are dispatched by the overload
    system as a final step by the overload system. Please note that these
    finalizers run even when the overloaded system encountered an error.

    Parameters
    ----------
    name: str
      The name of the overloaded function for which to set the finalizer.
    func: Callable
      The function object to be dispatched as a final step by the overload
      system when dispatching the overload at the given name.
    """
    existing = self.getFinalizers()
    existing[name] = func
    self.__finalizer_map__ = {**existing, }

  def getFinalizers(self, ) -> dict[str, Callable]:
    """
    This method returns the mappings from overloaded names to assigned
    finalizer functions.

    Returns
    -------
    dict[str, Callable]
      Mapping from overloaded name to its assigned finalizer function.
    """
    return maybe(self.__finalizer_map__, dict())
