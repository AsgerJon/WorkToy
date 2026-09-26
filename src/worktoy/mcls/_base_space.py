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

  SigFunc: TypeAlias = tuple[TypeSig, Callable[..., Any]]
  SigFuncList: TypeAlias = list[SigFunc]
  OverloadMap: TypeAlias = dict[str, SigFuncList]
  FuncMap: TypeAlias = dict[str, Callable[..., Any]]
  Ambiguity: TypeAlias = tuple[str, TypeSig, Callable, Callable]
  Collected: TypeAlias = tuple[TypeSig, Callable[..., Any], int]
  CollectedList: TypeAlias = list[Collected]


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
  __ambiguous_overloads__: Optional[list[Ambiguity]] = None

  #  Public Variables
  loadSpaceHook = LoadSpaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getOverloads(self, ) -> OverloadMap:
    """
    The 'getOverloads' method returns the concrete signatures the class
    body registered itself, as a mapping from each overloaded name to its
    list of '(TypeSig, function)' pairs in registration order. The
    concrete signatures expanded from a variadic declaration are
    included. Inherited registrations are not; see 'collectOverloads'.
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

  def getAmbiguousOverloads(self, ) -> list[Ambiguity]:
    """
    The 'getAmbiguousOverloads' method returns the signatures that two
    variadic declarations in the class body both expanded, for different
    functions. Each entry is a '(name, sig, oldFunc, newFunc)' tuple. An
    entry remains only while no explicit declaration of the signature has
    settled the ambiguity; 'LoadSpaceHook.postCompilePhase' raises for any
    entry still present when the class compiles.
    """
    return maybe(self.__ambiguous_overloads__, [])

  def _getLookupOrder(self, ) -> list[type]:
    """
    The '_getLookupOrder' method returns the classes after the class under
    construction in its method resolution order. A namespace created with
    '_strictMRO=False' for bases admitting no consistent order has none,
    and falls back to each base's own order, bases left to right, with
    repeated classes kept at their first position.
    """
    mro = self.getMRO()
    if mro is not None:
      return [*mro, ]
    out = []
    for base in self.getBases():
      for cls in base.__mro__:
        if cls not in out:
          out.append(cls)
    return out

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
    registers under the overloaded name.

    Colliding registrations of equal signatures resolve by kind. An
    explicit declaration displaces a concrete signature expanded from a
    variadic declaration, two such expanded signatures from different
    functions mark the signature as ambiguous (resolved later unless an
    explicit declaration arrives), and two explicit declarations of the
    same signature with different functions raise 'DuplicateSignature' on
    the spot.

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
      If the class body explicitly declares the same signature twice
      under this name with different functions.
    """
    existing = self.getOverloads()
    sigFuncs = existing.get(name, [])
    for index, (oldSig, oldFunc) in enumerate(sigFuncs):
      if oldSig == sig:
        self._resolveCollision(name, sigFuncs, index, sig, func)
        break
    else:
      sigFuncs.append((sig, func,))
    existing[name] = sigFuncs
    self.__overload_map__ = existing

  def _resolveCollision(
      self,
      name: str,
      sigFuncs: SigFuncList,
      index: int,
      sig: TypeSig,
      func: Callable,
  ) -> None:
    """
    The '_resolveCollision' method settles two registrations of equal
    signatures in the class body. Signatures expanded from a variadic
    declaration carry the '__expanded_from_variadic__' marking and rank
    below explicit declarations: an explicit declaration displaces an
    expanded one, an expanded one never displaces anything, and two
    expanded ones from different functions mark the signature ambiguous
    until an explicit declaration settles it. Two explicit declarations
    with different functions raise 'DuplicateSignature' immediately.

    Parameters
    ----------
    name: str
      The overloaded name under which the collision occurred.
    sigFuncs: SigFuncList
      Spells out to 'list[tuple[TypeSig, Callable]]'. The live list of
      registrations for 'name', mutated in place.
    index: int
      The position in 'sigFuncs' of the registration already stored.
    sig: TypeSig
      The arriving signature object, equal to the stored one.
    func: Callable
      The arriving function object.

    Raises
    ------
    DuplicateSignature
      If both registrations are explicit declarations of different
      functions.
    """
    oldSig, oldFunc = sigFuncs[index]
    newArtifact = getattr(sig, '__expanded_from_variadic__', False)
    oldArtifact = getattr(oldSig, '__expanded_from_variadic__', False)
    if newArtifact and oldArtifact:
      if oldFunc is not func:
        ambiguous = self.getAmbiguousOverloads()
        ambiguous.append((name, sig, oldFunc, func,))
        self.__ambiguous_overloads__ = ambiguous
      return
    if newArtifact:
      #  An explicit declaration already holds the slot.
      return
    if oldArtifact:
      #  The explicit declaration takes the place of the expanded one at
      #  the end of the list, and settles any ambiguity recorded for it.
      del sigFuncs[index]
      sigFuncs.append((sig, func,))
      self._settleAmbiguity(name, sig)
      return
    if oldFunc is not func:
      raise DuplicateSignature(sig, oldFunc, func)

  def _settleAmbiguity(self, name: str, sig: TypeSig) -> None:
    """
    The '_settleAmbiguity' method removes the ambiguity entries recorded
    for 'sig' under 'name', once an explicit declaration has claimed the
    signature.
    """
    ambiguous = self.getAmbiguousOverloads()
    remaining = []
    for entry in ambiguous:
      if entry[0] == name and entry[1] == sig:
        continue
      remaining.append(entry)
    self.__ambiguous_overloads__ = remaining

  def addVariadic(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    The 'addVariadic' method registers a variadic '(TypeSig, func)' pair
    under 'name'. The 'TypeSig' must carry a trailing 'ARGS' sentinel as
    its last raw type. The dispatcher matches variadic signatures by
    walking them in order rather than by hash lookup, and the first
    registered one wins.
    """
    existing = self.getVariadics()
    existing[name] = [*existing.get(name, []), (sig, func,)]
    self.__variadic_overload_map__ = existing

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
    """
    existing = self.getFallbacks()
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
    """
    existing = self.getFinalizers()
    existing[name] = func
    self.__finalizer_map__ = existing
