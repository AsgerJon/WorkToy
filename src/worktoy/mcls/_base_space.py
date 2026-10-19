"""
BaseSpace provides the namespace class used by worktoy.mcls.BaseMeta
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..dispatch import TypeSig, Dispatcher
from ..utilities import maybe
from ..waitaminute.dispatch import DuplicateSignature
from . import AbstractNamespace
from .space_hooks import LoadSpaceHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Callable, Any, Optional

  from ..dispatch import overload

  SigFunc: TypeAlias = tuple[TypeSig, Callable[..., Any]]
  SigFuncList: TypeAlias = list[SigFunc]
  OverloadMap: TypeAlias = dict[str, SigFuncList]
  FuncMap: TypeAlias = dict[str, Callable[..., Any]]
  Collected: TypeAlias = tuple[TypeSig, Callable[..., Any], int]
  CollectedList: TypeAlias = list[Collected]
  Claim: TypeAlias = tuple[overload, str]


class BaseSpace(AbstractNamespace):
  """
  BaseSpace is the namespace used by BaseMeta. It enables function
  overloading and related features via hook registration.

  Classes defined using this namespace support method overloading through
  hooks installed automatically in the class body. These hooks handle
  overload collection, dispatch construction, and support for 'THIS' as a
  placeholder during class creation.

  Own and inherited registrations
  -------------------------------
  The namespace records only the registrations its own class body makes.
  Registrations from other classes are merged in when the class compiles,
  by walking the method resolution order of the class under
  construction, which gives the same precedence Python gives plain
  methods:

  - The class body's own registrations come first.
  - Each class in the method resolution order then contributes its own
    registrations, in that order. A signature equal to one already
    collected is skipped, so the nearest class wins it.
  - The walk stops at the first class that holds a plain definition of
    the name, which shadows every overload beyond it.

  Signatures that differ merge, so the finished 'Dispatcher' accepts
  every call that any contributing class accepts. Each collected
  registration records its distance: 0 for the class body's own, 1 for
  the nearest contributing class, and so on. The 'Dispatcher' tries the
  nearest registrations first when matching by type and by 'isinstance',
  and the farthest first when casting, so that a signature added in a
  subclass never redirects a call a parent already handled through a
  cast. Registrations are kept in lists rather than in dicts keyed by
  signature, since a signature holding 'THIS' hashes differently before
  and after its class exists.

  The overload mechanism and other behavior are defined in
  'worktoy.mcls.space_hooks'. This namespace is returned from
  BaseMeta.__prepare__.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __overload_map__: Optional[OverloadMap] = None
  __variadic_overload_map__: Optional[OverloadMap] = None
  __fallback_map__: Optional[FuncMap] = None
  __finalizer_map__: Optional[FuncMap] = None
  __plain_names__: Optional[tuple[str, ...]] = None
  __claimed_overloads__: Optional[tuple[Claim, ...]] = None

  #  Public Variables
  loadSpaceHook = LoadSpaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getOverloads(self, ) -> OverloadMap:
    """
    The 'getOverloads' method returns the concrete signatures the class
    body registered itself, as a mapping from each overloaded name to its
    list of '(TypeSig, function)' pairs in registration order. Inherited
    registrations are not included; see 'collectOverloads'.
    """
    return maybe(self.__overload_map__, dict())

  def getVariadics(self, ) -> OverloadMap:
    """
    The 'getVariadics' method returns the variadic signatures the class
    body registered itself, as a mapping from each overloaded name to its
    list of '(TypeSig, function)' pairs, each signature ending in an
    'ARGS' entry. Inherited registrations are not included; see
    'collectVariadics'.
    """
    return maybe(self.__variadic_overload_map__, dict())

  def getFallbacks(self) -> FuncMap:
    """
    The 'getFallbacks' method returns the mapping from overloaded names to
    the fallback functions the class body registered itself.
    """
    return maybe(self.__fallback_map__, dict())

  def getFinalizers(self, ) -> FuncMap:
    """
    The 'getFinalizers' method returns the mapping from overloaded names
    to the finalizer functions the class body registered itself.
    """
    return maybe(self.__finalizer_map__, dict())

  def getPlainNames(self, ) -> tuple[str, ...]:
    """
    The 'getPlainNames' method returns the names the class body bound to
    something other than an 'overload', in the order first bound. A value
    another hook claims, such as an 'EZField', is among them, since it
    never reaches the namespace itself.
    """
    return maybe(self.__plain_names__, ())

  def getClaimedName(self, ov: overload) -> Optional[str]:
    """
    The 'getClaimedName' method returns the name under which the class
    body first bound the 'overload' object 'ov', or None when the class
    body has not bound it. The record belongs to the namespace, so a
    second class binding the same object starts without one.
    """
    for claimed, name in maybe(self.__claimed_overloads__, ()):
      if claimed is ov:
        return name
    return None

  def hasOverloads(self, name: str) -> bool:
    """
    The 'hasOverloads' method reports whether the class body registered
    anything under 'name': a concrete or variadic signature, a fallback
    or a finalizer. Registrations inherited from other classes do not
    count.
    """
    registries = (
      self.getOverloads(),
      self.getVariadics(),
      self.getFallbacks(),
      self.getFinalizers(),
    )
    present = any(name in registry for registry in registries)
    return True if present else False

  @staticmethod
  def _definesPlainly(cls: type, name: str) -> bool:
    """
    The '_definesPlainly' method reports whether 'cls' holds 'name' as a
    definition of its own that no overload may shadow. That is every value
    in its attributes except a 'Dispatcher' its 'BaseSpace' built from
    overload registrations. A 'Dispatcher' written in the class body
    itself counts as a plain definition, and so does anything a class not
    built by 'BaseSpace' holds under 'name'.
    """
    if name not in cls.__dict__:
      return False
    if not isinstance(cls.__dict__[name], Dispatcher):
      return True
    space = cls.__dict__.get('__namespace__', None)
    if isinstance(space, BaseSpace):
      #  A body-written 'Dispatcher' is stored in the namespace itself,
      #  whereas one built from registrations is added on compilation.
      return True if dict.__contains__(space, name) else False
    return True

  def _getInheritedSpaces(self, name: str) -> list[BaseSpace]:
    """
    The '_getInheritedSpaces' method returns the namespaces of the classes
    that may contribute registrations under 'name' to the class under
    construction, in the order of its method resolution order.

    The walk stops at the first class holding a plain definition of
    'name', as decided by '_definesPlainly'. That definition is what
    Python finds first, so no overload beyond it may shadow it. A
    'Dispatcher' that 'BaseSpace' built from registrations does not stop
    the walk: one is built for every inherited name, and only the
    registrations behind it count.
    """
    out = []
    for cls in self._getLookupOrder():
      if self._definesPlainly(cls, name):
        break
      space = cls.__dict__.get('__namespace__', None)
      if isinstance(space, BaseSpace):
        out.append(space)
    return out

  def _getLookupSpaces(self, ) -> list[BaseSpace]:
    """
    The '_getLookupSpaces' method returns the namespaces of every class in
    the lookup order built by 'BaseSpace', whether or not a plain
    definition shadows them for a given name.
    """
    out = []
    for cls in self._getLookupOrder():
      space = cls.__dict__.get('__namespace__', None)
      if isinstance(space, BaseSpace):
        out.append(space)
    return out

  def getOverloadNames(self, ) -> list[str]:
    """
    The 'getOverloadNames' method returns every name that the class body
    or any class in its lookup order registered anything under, in order
    of first appearance.
    """
    out = []
    for space in (self, *self._getLookupSpaces()):
      maps = (
        space.getOverloads(),
        space.getVariadics(),
        space.getFallbacks(),
        space.getFinalizers(),
      )
      for registry in maps:
        for name in registry:
          if name not in out:
            out.append(name)
    return out

  @staticmethod
  def _mergeSigFuncs(
      collected: CollectedList,
      more: SigFuncList,
      distance: int,
  ) -> None:
    """
    The '_mergeSigFuncs' method appends to 'collected' each pair from
    'more' whose signature equals none already collected, together with
    'distance'. Entries collected earlier come from nearer classes, so
    they keep an equal signature.
    """
    for sig, func in more:
      for existing, _, __ in collected:
        if existing == sig:
          break
      else:
        collected.append((sig, func, distance,))

  def collectOverloads(self, name: str) -> CollectedList:
    """
    The 'collectOverloads' method returns the concrete signatures the
    class under construction dispatches under 'name', as '(TypeSig,
    function, distance)' entries. The class body's own registrations come
    first at distance 0, followed by those of each class in the method
    resolution order not shadowed by a plain definition, skipping
    signatures a nearer class already registered.
    """
    out = []
    spaces = (self, *self._getInheritedSpaces(name))
    for distance, space in enumerate(spaces):
      sigFuncs = space.getOverloads().get(name, [])
      self._mergeSigFuncs(out, sigFuncs, distance)
    return out

  def collectVariadics(self, name: str) -> CollectedList:
    """
    The 'collectVariadics' method returns the variadic signatures the
    class under construction dispatches under 'name', as '(TypeSig,
    function, distance)' entries merged in the same way as
    'collectOverloads'.
    """
    out = []
    spaces = (self, *self._getInheritedSpaces(name))
    for distance, space in enumerate(spaces):
      sigFuncs = space.getVariadics().get(name, [])
      self._mergeSigFuncs(out, sigFuncs, distance)
    return out

  def collectFallback(self, name: str) -> Optional[Callable]:
    """
    The 'collectFallback' method returns the fallback the class under
    construction uses under 'name': its own, or else that of the nearest
    class in the method resolution order not shadowed by a plain
    definition. Returns None when there is none.
    """
    for space in (self, *self._getInheritedSpaces(name)):
      fallback = space.getFallbacks().get(name, None)
      if fallback is not None:
        return fallback
    return None

  def collectFinalizer(self, name: str) -> Optional[Callable]:
    """
    The 'collectFinalizer' method returns the finalizer the class under
    construction uses under 'name', found the same way as
    'collectFallback'. Returns None when there is none.
    """
    for space in (self, *self._getInheritedSpaces(name)):
      finalizer = space.getFinalizers().get(name, None)
      if finalizer is not None:
        return finalizer
    return None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addOverload(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    The 'addOverload' method records a concrete signature the class body
    registers under the overloaded name. The same function registered
    again under an equal signature, as when an overload is bound again
    under its own name, changes nothing, and a different function under an
    equal signature raises 'DuplicateSignature' on the spot.

    Parameters
    ----------
    name: str
      The name of the overloaded function.
    sig: TypeSig
      The type signature for the overload.
    func: Callable
      The function object to be dispatched when given arguments matching
      the given type signature.

    Raises
    ------
    DuplicateSignature
      If the class body declares the same signature twice under this name
      with different functions.
    """
    existing = self.getOverloads()
    sigFuncs = existing.get(name, [])
    for oldSig, oldFunc in sigFuncs:
      if oldSig == sig:
        if oldFunc is not func:
          raise DuplicateSignature(sig, oldFunc, func)
        break
    else:
      sigFuncs.append((sig, func,))
    existing[name] = sigFuncs
    self.__overload_map__ = existing

  def addVariadic(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    The 'addVariadic' method registers a variadic '(TypeSig, func)' pair
    under 'name'. The 'TypeSig' must carry a trailing 'ARGS' sentinel as
    its last raw type. The dispatcher matches a call against the variadic
    signatures by exact type first, the prefix and the trailing type as
    a hash key, then through 'isinstance', and of several accepting one
    call the most recent declaration of the nearest class wins.
    """
    existing = self.getVariadics()
    existing[name] = [*existing.get(name, []), (sig, func,)]
    self.__variadic_overload_map__ = existing

  def addPlainName(self, name: str) -> None:
    """
    The 'addPlainName' method records that the class body bound 'name' to
    something other than an 'overload'.
    """
    existing = self.getPlainNames()
    if name not in existing:
      self.__plain_names__ = (*existing, name)

  def addClaimedName(self, ov: overload, name: str) -> None:
    """
    The 'addClaimedName' method records that the class body bound the
    'overload' object 'ov' under 'name', the name a later binding of the
    same object in this class body is read as an alias of.
    """
    existing = maybe(self.__claimed_overloads__, ())
    self.__claimed_overloads__ = (*existing, (ov, name))

  def addFallback(self, name: str, func: Callable) -> None:
    """
    The 'addFallback' method records the fallback function for the
    overloaded name. These fallbacks are dispatched by the overload
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

    Raises
    ------
    DuplicateSignature
      If the class body already registered a different fallback under
      this name, as for two explicit declarations of one signature. A
      fallback inherited from another class is not on record here, so a
      subclass may replace it.
    """
    existing = self.getFallbacks()
    oldFunc = existing.get(name, None)
    if oldFunc is not None and oldFunc is not func:
      raise DuplicateSignature('fallback', oldFunc, func)
    existing[name] = func
    self.__fallback_map__ = existing

  def addFinalizer(self, name: str, func: Callable) -> None:
    """
    The 'addFinalizer' method records the finalizer function for the
    overloaded name. Finalizer functions are dispatched by the overload
    system as a final step, and run even when the dispatched call raised.

    Parameters
    ----------
    name: str
      The name of the overloaded function for which to set the finalizer.
    func: Callable
      The function object to be dispatched as a final step by the overload
      system when dispatching the overload at the given name.

    Raises
    ------
    DuplicateSignature
      If the class body already registered a different finalizer under
      this name. A finalizer inherited from another class may be
      replaced.
    """
    existing = self.getFinalizers()
    oldFunc = existing.get(name, None)
    if oldFunc is not None and oldFunc is not func:
      raise DuplicateSignature('finalizer', oldFunc, func)
    existing[name] = func
    self.__finalizer_map__ = existing
