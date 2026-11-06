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
from ..waitaminute.meta import MixedMethodKind
from . import AbstractNamespace
from .space_hooks import LoadSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
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
  A 'BaseObject' class declares overloads with '@overload' and inherits
  those of its bases. Its namespace must keep what the body declares at
  each name, and, as the class is compiled, gather what the bases
  declared. Which declarations a class inherits follows Python's lookup
  of the name, each dispatcher counting as a method that holds every
  overload its class answers: the body first, then each base in
  resolution order, the nearest class keeping an equal signature, and a
  plain definition hiding what lies behind it on its own branch. In a
  diamond whose other branch overloads the name, a class listing that
  branch first keeps what the branch inherits, since Python's lookup
  gives it the method of that branch, while a class listing the plain
  branch first takes the plain method.

  Two things differ from plain Python by design. The overloads of bases
  on different branches ahead of a plain definition merge into one
  dispatcher, where Python's lookup would give the method of the first
  base alone. And a plain method behind the overloads takes no call they
  refuse, where a chain of 'super()' calls would hand such a call on to
  it: once a class overloads a name, a plain method it inherits there
  takes no part in its dispatch. Each gathered
  declaration must carry how far from the class it comes, which decides
  the order of dispatch. An overloaded name is one kind of method, an
  instance method, a classmethod or a staticmethod: one body may not
  declare it as two, and a base declaring it as another kind than the
  nearer classes is hidden as a plain definition is.

  Implementation
  --------------

  'loadSpaceHook' records the declarations of the body through
  'addOverload', 'addVariadic', 'addFallback' and 'addFinalizer'; one body
  may not declare one signature, fallback or finalizer twice for
  different functions. 'collectOverloads', 'collectVariadics',
  'collectFallback' and 'collectFinalizer' gather the declarations of the
  body and of the 'BaseSpace' namespaces of the bases, with distances, 0
  for the body. 'addMethodKind' records the kind each name is declared
  as, refusing a second kind with 'MixedMethodKind', and
  '_getInheritedSpaces' passes over a base of another kind as it passes
  over a plain definition, so
  'collectMethodKind' gives the kind of the nearest class declaring the
  name. They are kept in lists rather than dictionaries keyed by
  signature, since a signature holding 'THIS' hashes differently once its
  class exists. The signature objects are shared with the dispatchers
  built from them, those of subclasses included, so nothing changes them
  in place once the class exists.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __overload_map__: Optional[OverloadMap] = None
  __variadic_overload_map__: Optional[OverloadMap] = None
  __flex_overload_map__: Optional[OverloadMap] = None
  __fallback_map__: Optional[FuncMap] = None
  __finalizer_map__: Optional[FuncMap] = None
  __plain_names__: Optional[tuple[str, ...]] = None
  __claimed_overloads__: Optional[tuple[Claim, ...]] = None
  __method_kinds__: Optional[dict[str, Any]] = None

  #  Public Variables
  loadSpaceHook = LoadSpaceHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getOverloads(self, ) -> OverloadMap:
    """
    The dispatchers of the class and of its subclasses need the concrete
    signatures this class body declared itself.

    Returns
    -------

    OverloadMap
      A 'dict[str, list[tuple[TypeSig, Callable]]]', in declaration order.
    """
    return maybe(self.__overload_map__, dict())

  def getVariadics(self, ) -> OverloadMap:
    """
    As 'getOverloads', for the signatures ending in an 'ARGS'.

    Returns
    -------

    OverloadMap
      A 'dict[str, list[tuple[TypeSig, Callable]]]', in declaration order.
    """
    return maybe(self.__variadic_overload_map__, dict())

  def getFlexes(self, ) -> OverloadMap:
    """
    As 'getOverloads', for the flexible declarations of more than three
    classes, each signature in the order the function takes its
    arguments.

    Returns
    -------

    OverloadMap
      A 'dict[str, list[tuple[TypeSig, Callable]]]', in declaration order.
    """
    return maybe(self.__flex_overload_map__, dict())

  def getFallbacks(self) -> FuncMap:
    """
    The fallbacks this class body declared itself, by name.

    Returns
    -------

    FuncMap
      A 'dict[str, Callable]'.
    """
    return maybe(self.__fallback_map__, dict())

  def getFinalizers(self, ) -> FuncMap:
    """
    The finalizers this class body declared itself, by name.

    Returns
    -------

    FuncMap
      A 'dict[str, Callable]'.
    """
    return maybe(self.__finalizer_map__, dict())

  def getMethodKinds(self) -> dict[str, Any]:
    """
    The dispatchers of the class and of its subclasses need the kind of
    method this class body declared each overloaded name as.

    Returns
    -------

    dict[str, Any]
      From each name to 'classmethod', 'staticmethod', or 'None' for an
      instance method.
    """
    return maybe(self.__method_kinds__, dict())

  def _getDeclaredKind(self, name: str) -> tuple:
    """
    'None' is the kind of an instance method, so whether this body declared
    the name at all needs an answer of its own.

    Returns
    -------

    tuple
      The kind in a one-element tuple, or an empty tuple when the body
      declared nothing at the name.
    """
    kinds = self.getMethodKinds()
    try:
      kind = kinds[name]
    except KeyError:
      return ()
    else:
      return (kind,)

  def getPlainNames(self, ) -> tuple[str, ...]:
    """
    A name may not be both overloaded and defined plainly in one body, so
    the plain names must be known, including a value another hook claims,
    such as an 'EZField', which never reaches the dictionary.

    Returns
    -------

    tuple[str, ...]
      The plainly bound names, in order first bound.
    """
    return maybe(self.__plain_names__, ())

  def getClaimedName(self, ov: overload) -> Optional[str]:
    """
    One 'overload' object bound twice in a body would register its function
    under two names; the first name must be known to refuse the second.

    Parameters
    ----------

    ov : overload
      The 'overload' object.

    Returns
    -------

    str or None
      The name it was bound to in this body, or 'None'.
    """
    for claimed, name in maybe(self.__claimed_overloads__, ()):
      if claimed is ov:
        return name
    return None

  def hasOverloads(self, name: str) -> bool:
    """
    A plain binding at a name the body overloaded must be refused.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    bool
      Whether the body declared anything at the name; inherited
      declarations do not count.
    """
    registries = (
      self.getOverloads(),
      self.getVariadics(),
      self.getFlexes(),
      self.getFallbacks(),
      self.getFinalizers(),
    )
    present = any(name in registry for registry in registries)
    return True if present else False

  @staticmethod
  def _definesPlainly(cls: type, name: str) -> bool:
    """
    The search for inherited declarations must not pass a class holding a
    plain definition of the name, which hides what lies behind it, but
    must pass a dispatcher a 'BaseSpace' built from declarations, since
    every class has one for each inherited name.

    Implementation
    --------------

    Anything held at the name counts, except a 'Dispatcher', which the
    namespace of a class builds from declarations.

    Parameters
    ----------

    cls : type
      A class along the resolution order.

    name : str
      The name.

    Returns
    -------

    bool
      Whether the class defines the name plainly.
    """
    if name not in cls.__dict__:
      return False
    return False if isinstance(cls.__dict__[name], Dispatcher) else True

  @staticmethod
  def _getOwnSpace(cls: type) -> Optional[BaseSpace]:
    try:
      space = cls.__dict__['__namespace__']
    except KeyError:
      #  This branch is reached by the following:
      #  - The class was built by no worktoy metaclass, as a plain mixin or
      #    'object'
      return None
    if isinstance(space, BaseSpace):
      return space
    #  The rest of the method is reached by the following:
    #  - The class was built by a worktoy metaclass whose namespace is no
    #    'BaseSpace', as 'Object' and the sentinels are
    return None

  def _hidesInherited(self, cls: type, name: str, kind: tuple) -> bool:
    """
    A class along the resolution order may hide the declarations behind it
    at a name, so the overloads behind it are none of the new class's. A
    plain definition hides them, and so does a declaration of the name as
    another kind of method than the nearer classes declare, which
    overrides them as a plain definition does.

    Parameters
    ----------

    cls : type
      A class along the resolution order.

    name : str
      The name.

    kind : tuple
      The kind the nearer classes declare, in a one-element tuple, or an
      empty tuple when none of them declares the name.

    Returns
    -------

    bool
      Whether the class hides what lies behind it at the name.
    """
    if self._definesPlainly(cls, name):
      return True
    space = self._getOwnSpace(cls)
    if space is None:
      return False
    found = space._getDeclaredKind(name)
    return True if kind and found and found[0] is not kind[0] else False

  def _isReachedAlong(
      self,
      route: list[type],
      target: type,
      name: str,
      kind: tuple,
  ) -> bool:
    """
    A class is inherited along a route, a resolution order, when it lies on
    the route and no class ahead of it there hides the name.

    Parameters
    ----------

    route : list[type]
      The resolution order of the new class, or of a base it gathers, the
      class itself left out.

    target : type
      The class asked about.

    name : str
      The name.

    kind : tuple
      As for '_hidesInherited'.

    Returns
    -------

    bool
      Whether the route reaches the class without passing one hiding the
      name.
    """
    if target not in route:
      return False
    for cls in route[:route.index(target)]:
      if self._hidesInherited(cls, name, kind):
        return False
    return True

  def _getInheritedSpaces(self, name: str) -> list[BaseSpace]:
    """
    A class inherits the overloads of a name from its bases as Python's
    lookup would hand it their methods, each dispatcher counting as a
    method that holds every overload its class answers: a plain
    definition, or a declaration of another kind of method, hides what
    lies behind it, but only on its own branch. In a diamond whose plain
    branch comes second, a
    class listing the overloading branch first must keep what that branch
    inherits from the ancestor both share, although the plain branch stands
    between them in the order of the class:

      class Badge(LabelledShape, FixedShape):   # FixedShape plain
        pass                                    # Shape overloads 'int'

    'Badge().scale(2)' must reach 'Shape' through 'LabelledShape', as
    'LabelledShape().scale(2)' does. A class listing the plain branch first
    takes the plain method instead. The plain method of 'FixedShape' takes
    no call the overloads of 'Badge' refuse, although a chain of 'super()'
    calls would hand it one, since a plain method a class inherits at an
    overloaded name takes no part in its dispatch.

    Implementation
    --------------

    The resolution order of the new class is walked. A class is gathered
    when it holds a 'BaseSpace' namespace, hides nothing, and lies on a
    route that reaches it without passing a class that hides the name. The
    routes are the order of the new class and the order of each base
    gathered so far, so before the first class hiding the name every base
    is gathered, and past it only what a gathered base inherits itself. The
    kind of method is the one the body declares, or else the one the first
    base declaring the name declares.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    list[BaseSpace]
      Their namespaces, in resolution order.
    """
    out = []
    kind = self._getDeclaredKind(name)
    lookupOrder = self._getLookupOrder()
    routes = [lookupOrder]
    for cls in lookupOrder:
      if self._hidesInherited(cls, name, kind):
        continue
      space = self._getOwnSpace(cls)
      if space is None:
        continue
      if not any(self._isReachedAlong(r, cls, name, kind) for r in routes):
        #  This branch is reached by the following:
        #  - A class hiding the name stands ahead of this base in the order
        #    of the new class, and no base gathered before inherits this one
        #    past such a class
        continue
      if not kind:
        kind = space._getDeclaredKind(name)
      out.append(space)
      routes.append([*cls.__mro__[1:]])
    return out

  def _getLookupSpaces(self, ) -> list[BaseSpace]:
    out = []
    for cls in self._getLookupOrder():
      space = cls.__dict__.get('__namespace__', None)
      if isinstance(space, BaseSpace):
        out.append(space)
    return out

  def getOverloadNames(self, ) -> list[str]:
    """
    A dispatcher must be built for every name the body or a base declared
    overloads at.

    Returns
    -------

    list[str]
      The names, in order of first appearance.
    """
    out = []
    for space in (self, *self._getLookupSpaces()):
      maps = (
        space.getOverloads(),
        space.getVariadics(),
        space.getFlexes(),
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
    for sig, func in more:
      for existing, _, __ in collected:
        if existing == sig:
          break
      else:
        collected.append((sig, func, distance,))

  def collectOverloads(self, name: str) -> CollectedList:
    """
    The dispatcher of a name needs every concrete signature the class
    answers to, its own and the inherited ones, with their distances.

    Implementation
    --------------

    The body comes first at distance 0, then each namespace from
    '_getInheritedSpaces' at its position; a signature equal to one
    gathered already is skipped, so the nearer class keeps it.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    CollectedList
      A 'list[tuple[TypeSig, Callable, int]]' of signature, function and
      distance.
    """
    out = []
    spaces = (self, *self._getInheritedSpaces(name))
    for distance, space in enumerate(spaces):
      sigFuncs = space.getOverloads().get(name, [])
      self._mergeSigFuncs(out, sigFuncs, distance)
    return out

  def collectVariadics(self, name: str) -> CollectedList:
    """
    As 'collectOverloads', for the signatures ending in an 'ARGS'.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    CollectedList
      A 'list[tuple[TypeSig, Callable, int]]'.
    """
    out = []
    spaces = (self, *self._getInheritedSpaces(name))
    for distance, space in enumerate(spaces):
      sigFuncs = space.getVariadics().get(name, [])
      self._mergeSigFuncs(out, sigFuncs, distance)
    return out

  def collectFlexes(self, name: str) -> CollectedList:
    """
    As 'collectOverloads', for the flexible declarations of more than three
    classes. Two declarations of the same classes in different orders are
    one declaration, so the nearer class keeps it.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    CollectedList
      A 'list[tuple[TypeSig, Callable, int]]'.
    """
    out = []
    spaces = (self, *self._getInheritedSpaces(name))
    for distance, space in enumerate(spaces):
      for sig, func in space.getFlexes().get(name, []):
        bag = sig.getBag()
        for existing, _, __ in out:
          if existing.getBag() == bag:
            break
        else:
          out.append((sig, func, distance,))
    return out

  def collectMethodKind(self, name: str) -> Any:
    """
    The dispatcher of a name must be the kind of method the nearest class
    declaring the name made it.

    Implementation
    --------------

    The body and the namespaces from '_getInheritedSpaces', which agree
    on the kind, are asked in order.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    Any
      'classmethod', 'staticmethod', or 'None' for an instance method.
    """
    for space in (self, *self._getInheritedSpaces(name)):
      found = space._getDeclaredKind(name)
      if found:
        return found[0]
    return None

  def collectFallback(self, name: str) -> Optional[Callable]:
    """
    The dispatcher of a name needs the fallback of the nearest class
    declaring one, up to the first plain definition.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    Callable or None
      The fallback, or 'None'.
    """
    for space in (self, *self._getInheritedSpaces(name)):
      fallback = space.getFallbacks().get(name, None)
      if fallback is not None:
        return fallback
    return None

  def collectFinalizer(self, name: str) -> Optional[Callable]:
    """
    As 'collectFallback', for the finalizer.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    Callable or None
      The finalizer, or 'None'.
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
    Two functions declared at one signature in one body would leave
    dispatch undecided, while one declaration reached twice is harmless.

    Parameters
    ----------

    name : str
      The name.

    sig : TypeSig
      The signature, a copy owned by this namespace.

    func : Callable
      The function, or a 'PermuterMethod' of a flexible declaration.

    Raises
    ------

    DuplicateSignature
      An equal signature is declared for a different function, or a
      flexible declaration of the same classes is.
    """
    bag = sig.getBag()
    for flexSig, flexFunc in self.getFlexes().get(name, []):
      if flexSig.getBag() == bag and flexFunc is not func:
        raise DuplicateSignature(sig, flexFunc, func)
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

  def addFlex(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    A flexible declaration of more than three classes stands for every
    order of its classes, so one body declaring those classes again for a
    different function, flexibly or as one order, leaves dispatch
    undecided, as two functions at one signature do.

    Parameters
    ----------

    name : str
      The name.

    sig : TypeSig
      The signature in the order the function takes its arguments, a copy
      owned by this namespace.

    func : Callable
      The function.

    Raises
    ------

    DuplicateSignature
      The same classes are declared for a different function, flexibly or
      as one order.
    """
    bag = sig.getBag()
    for oldSig, oldFunc in self.getOverloads().get(name, []):
      if oldSig.getBag() == bag and oldFunc is not func:
        raise DuplicateSignature(sig, oldFunc, func)
    existing = self.getFlexes()
    flexes = existing.get(name, [])
    for oldSig, oldFunc in flexes:
      if oldSig.getBag() == bag:
        if oldFunc is not func:
          raise DuplicateSignature(sig, oldFunc, func)
        break
    else:
      flexes.append((sig, func,))
    existing[name] = flexes
    self.__flex_overload_map__ = existing

  def addVariadic(self, name: str, sig: TypeSig, func: Callable) -> None:
    """
    As 'addOverload', for a signature ending in an 'ARGS'. Different
    variadic signatures accepting one call are no conflict; the most
    recent declaration of the nearest class takes it.

    Parameters
    ----------

    name : str
      The name.

    sig : TypeSig
      The signature.

    func : Callable
      The function.

    Raises
    ------

    DuplicateSignature
      An equal signature is declared for a different function.
    """
    existing = self.getVariadics()
    sigFuncs = existing.get(name, [])
    for oldSig, oldFunc in sigFuncs:
      if oldSig == sig:
        if oldFunc is not func:
          raise DuplicateSignature(sig, oldFunc, func)
        break
    else:
      sigFuncs.append((sig, func,))
    existing[name] = sigFuncs
    self.__variadic_overload_map__ = existing

  def addMethodKind(self, name: str, kind: Any) -> None:
    """
    One dispatcher stands at an overloaded name and passes one receiver
    to every function, so one body declares the name as one kind of
    method.

    Parameters
    ----------

    name : str
      The name.

    kind : Any
      'classmethod', 'staticmethod', or 'None' for an instance method.

    Raises
    ------

    MixedMethodKind
      The body declared the name as another kind already.
    """
    kinds = self.getMethodKinds()
    try:
      existing = kinds[name]
    except KeyError:
      kinds[name] = kind
      self.__method_kinds__ = kinds
    else:
      if existing is not kind:
        raise MixedMethodKind(self.getClassName(), name, (existing, kind))

  def addPlainName(self, name: str) -> None:
    """
    'LoadSpaceHook' records each name bound to anything but an
    'overload'.
    """
    existing = self.getPlainNames()
    if name not in existing:
      self.__plain_names__ = (*existing, name)

  def removePlainName(self, name: str) -> None:
    """
    A plain definition deleted from the body no longer conflicts with
    overloads at its name.
    """
    existing = self.getPlainNames()
    self.__plain_names__ = (*(n for n in existing if n != name),)

  def addClaimedName(self, ov: overload, name: str) -> None:
    """
    'LoadSpaceHook' records the name an 'overload' object was bound to, so
    a second binding of it can be refused naming the first.
    """
    existing = maybe(self.__claimed_overloads__, ())
    self.__claimed_overloads__ = (*existing, (ov, name))

  def addFallback(self, name: str, func: Callable) -> None:
    """
    One body may declare one fallback per name; a subclass may replace an
    inherited one, which is not on record here.

    Parameters
    ----------

    name : str
      The name.

    func : Callable
      The fallback.

    Raises
    ------

    DuplicateSignature
      The body declared a different fallback at the name already.
    """
    existing = self.getFallbacks()
    oldFunc = existing.get(name, None)
    if oldFunc is not None and oldFunc is not func:
      raise DuplicateSignature('fallback', oldFunc, func)
    existing[name] = func
    self.__fallback_map__ = existing

  def addFinalizer(self, name: str, func: Callable) -> None:
    """
    As 'addFallback', for the finalizer.

    Parameters
    ----------

    name : str
      The name.

    func : Callable
      The finalizer.

    Raises
    ------

    DuplicateSignature
      The body declared a different finalizer at the name already.
    """
    existing = self.getFinalizers()
    oldFunc = existing.get(name, None)
    if oldFunc is not None and oldFunc is not func:
      raise DuplicateSignature('finalizer', oldFunc, func)
    existing[name] = func
    self.__finalizer_map__ = existing
