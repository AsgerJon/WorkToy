"""
BaseSpace provides the namespace class used by worktoy.mcls.BaseMeta
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..dispatch import TypeSig
from ..utilities import maybe
from ..waitaminute.dispatch import DuplicateSignature
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
  __own_overload_keys__ = None
  __ambiguous_overloads__ = None

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
              self.addOverload(overloadName, sig, func, _inherited=True)
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

  def addOverload(
      self, name: str, sig: TypeSig, func: Callable, **kwargs,
  ) -> None:
    """
    The 'addOverload' method records the mapping from type signature to
    function object under the overloaded name.

    Colliding registrations of equal signatures resolve by origin and
    kind. A registration belonging to the class body itself always
    displaces one inherited from a base class. Among the class body's
    own registrations, an explicit declaration displaces a concrete
    signature expanded from a variadic declaration, two such expanded
    signatures from different functions mark the signature as
    ambiguous (resolved later unless an explicit declaration arrives),
    and two explicit declarations of the same signature with different
    functions raise 'DuplicateSignature' on the spot.

    Parameters
    ----------
    name: str
      The name of the overloaded function.
    sig: TypeSig
      The type signature for the overload.
    func: Callable
      The function object to be dispatched when given arguments matching
      the given type signature.
    **kwargs
      The '_inherited' keyword marks registrations copied from a base
      class namespace, which own registrations always displace.

    Raises
    ------
    DuplicateSignature
      If the class body explicitly declares the same signature twice
      under this name with different functions.
    """
    inherited = kwargs.get('_inherited', False)
    existing = self.getOverloads()
    if name not in existing:
      existing[name] = dict()
    sigFunc = existing[name]
    oldKey = None
    for key in sigFunc:
      if key == sig:
        oldKey = key
        break
    ownKeys = self.getOwnOverloadKeys()
    if oldKey is None:
      sigFunc[sig] = func
      if not inherited:
        ownKeys.add((name, sig))
        self.__own_overload_keys__ = ownKeys
    elif inherited:
      #  Collision among inherited registrations: the base processed
      #  later wins, preserving the pre-existing merge semantics.
      sigFunc[oldKey] = func
    elif (name, oldKey) not in ownKeys:
      #  An own declaration displaces an inherited registration. The
      #  old key is removed so the stored key carries the own
      #  declaration's expansion marking.
      del sigFunc[oldKey]
      sigFunc[sig] = func
      ownKeys.add((name, sig))
      self.__own_overload_keys__ = ownKeys
    else:
      self._resolveOwnCollision(name, sigFunc, oldKey, sig, func)
    self.__overload_map__ = {**existing, }

  def _resolveOwnCollision(
      self,
      name: str,
      sigFunc: SigFunc,
      oldKey: TypeSig,
      sig: TypeSig,
      func: Callable,
  ) -> None:
    """
    The '_resolveOwnCollision' method settles two registrations of equal
    signatures both declared in the class body itself. Signatures
    expanded from a variadic declaration carry the
    '__expanded_from_variadic__' marking and rank below explicit
    declarations: an explicit declaration displaces an expanded one,
    an expanded one never displaces anything, and two expanded ones
    from different functions mark the signature ambiguous until an
    explicit declaration settles it. Two explicit declarations with
    different functions raise 'DuplicateSignature' immediately.

    Parameters
    ----------
    name: str
      The overloaded name under which the collision occurred.
    sigFunc: SigFunc
      Spells out to 'dict[TypeSig, Callable]'. The live signature
      mapping for 'name', mutated in place.
    oldKey: TypeSig
      The signature object already stored, carrying its own expansion
      marking.
    sig: TypeSig
      The arriving signature object, equal to 'oldKey'.
    func: Callable
      The arriving function object.

    Raises
    ------
    DuplicateSignature
      If both registrations are explicit declarations of different
      functions.
    """
    newArtifact = getattr(sig, '__expanded_from_variadic__', False)
    oldArtifact = getattr(oldKey, '__expanded_from_variadic__', False)
    oldFunc = sigFunc[oldKey]
    if newArtifact and oldArtifact:
      if oldFunc is not func:
        ambiguous = self.getAmbiguousOverloads()
        ambiguous[(name, sig)] = (oldFunc, func)
        self.__ambiguous_overloads__ = ambiguous
      return
    if newArtifact:
      #  An explicit declaration already holds the slot.
      return
    if oldArtifact:
      del sigFunc[oldKey]
      sigFunc[sig] = func
      ambiguous = self.getAmbiguousOverloads()
      ambiguous.pop((name, sig), None)
      self.__ambiguous_overloads__ = ambiguous
      return
    if oldFunc is not func:
      raise DuplicateSignature(sig, oldFunc, func)

  def getOwnOverloadKeys(self, ) -> set:
    """
    The 'getOwnOverloadKeys' method returns the set of '(name, sig)'
    pairs registered by the class body itself, as opposed to those
    copied from base class namespaces. An empty set when nothing has
    been registered yet.

    Returns
    -------
    set[tuple[str, TypeSig]]
      The '(name, sig)' pairs the class body registered itself.
    """
    return maybe(self.__own_overload_keys__, set())

  def getAmbiguousOverloads(self, ) -> dict:
    """
    The 'getAmbiguousOverloads' method returns the mapping of
    '(name, sig)' pairs to the two function objects whose variadic
    declarations expanded to the same concrete signature. Entries
    remain only while no explicit declaration of the signature has
    settled the ambiguity; 'LoadSpaceHook.postCompilePhase' raises for
    any entry still present when the class compiles.

    Returns
    -------
    dict[tuple[str, TypeSig], tuple[Callable, Callable]]
      The unresolved ambiguous signature registrations.
    """
    return maybe(self.__ambiguous_overloads__, dict())

  def getOverloads(self, ) -> OverloadMap:
    """
    The 'getOverloads' method returns the mapping from each overloaded
    name to its own mapping from type signature to function object.

    Returns
    -------
    OverloadMap: TypeAlias = dict[str, dict[TypeSig, Callable]]
      Mapping from overloaded name to its mapping from type signature to
      function object.
    """
    return maybe(self.__overload_map__, dict())

  def addVariadic(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    The 'addVariadic' method registers a variadic '(TypeSig, func)' pair
    under 'name'. The 'TypeSig' must carry a trailing 'ARGS' sentinel as
    its last raw type. These pairs are stored in a list rather than a
    dict because 'ARGS' instances are not hashable and the dispatcher
    matches variadic sigs by structural iteration, not by hash lookup.
    """
    existing = self.getVariadics()
    if name not in existing:
      existing[name] = []
    existing[name] = [*existing[name], (sig, func,)]
    self.__variadic_overload_map__ = {**existing, }

  def getVariadics(self, ) -> VariadicMap:
    """
    The 'getVariadics' method returns the mapping from each overloaded
    name to its list of variadic '(TypeSig, func)' pairs, an empty dict
    when none have been registered.
    """
    return maybe(self.__variadic_overload_map__, {})

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
    self.__fallback_map__ = {**existing, }

  def getFallbacks(self) -> dict[str, Callable]:
    """
    The 'getFallbacks' method returns the mapping from overloaded names
    to their assigned fallback functions.

    Returns
    -------
    dict[str, Callable]
      Mapping from overloaded name to its assigned fallback function.
    """
    return maybe(self.__fallback_map__, dict())

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
    self.__finalizer_map__ = {**existing, }

  def getFinalizers(self, ) -> dict[str, Callable]:
    """
    The 'getFinalizers' method returns the mapping from overloaded names
    to their assigned finalizer functions.

    Returns
    -------
    dict[str, Callable]
      Mapping from overloaded name to its assigned finalizer function.
    """
    return maybe(self.__finalizer_map__, dict())
