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

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Callable, Any, Optional

  from ..dispatch import overload

  SigFunc: TypeAlias = tuple[TypeSig, Callable[..., Any]]
  SigFuncList: TypeAlias = list[SigFunc]
  OverloadMap: TypeAlias = dict[str, SigFuncList]
  FuncMap: TypeAlias = dict[str, Callable[..., Any]]
  FuncListMap: TypeAlias = dict[str, list[Callable[..., Any]]]
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
  the order of dispatch. An overloaded name may hold bound methods,
  classmethods and staticmethods together, each function keeping its
  kind. A bound method is reached through an instance and a staticmethod
  through the class, so the two never answer one call and may share a
  signature; any other two functions of one signature at a name would
  leave dispatch undecided. The fallbacks of a name are two, apart: the
  instance bound fallback takes a call through an instance that nothing
  accepts, and the class bound fallback takes such a call through the
  class. A fallback declared as a bound method is instance bound, one
  declared as a staticmethod is class bound, and one declared as a
  classmethod is both, so a name may hold a bound fallback and a static
  one, and any other two would leave it undecided which one takes a
  call. A base declaring the name as kinds none of which the nearer
  classes declare is hidden as a plain definition is.

  Implementation
  --------------

  'loadSpaceHook' records the declarations of the body through
  'addOverload', 'addVariadic', 'addFallback' and 'addFinalizer'; one body
  may not declare one signature or finalizer twice for different
  functions, nor two fallbacks that one call could reach.
  'collectOverloads', 'collectVariadics', 'collectFallbacks' and
  'collectFinalizer' gather the declarations of the body and of the
  'BaseSpace' namespaces of the bases, with distances, 0 for the body;
  'collectFallback' gives the nearest fallback alone, and
  'collectFallbacks' begins with it. 'addMethodKind' records the kinds
  each name is declared
  as and 'addFunctionKind' the kind of each function, and
  '_getInheritedSpaces' passes over a base sharing no kind with the
  nearer classes as it passes over a plain definition.
  'collectFunctionKinds' gathers the kind of every function at a name,
  from which 'LoadSpaceHook' builds the dispatchers, and
  'collectMethodKind' gives the first kind of the nearest class declaring
  the name. They are kept in lists rather than dictionaries keyed by
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
  __fallback_map__: Optional[FuncListMap] = None
  __finalizer_map__: Optional[FuncMap] = None
  __plain_names__: Optional[tuple[str, ...]] = None
  __claimed_overloads__: Optional[tuple[Claim, ...]] = None
  __method_kinds__: Optional[dict[str, tuple]] = None
  __function_kinds__: Optional[dict[str, list]] = None

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

  def getFallbacks(self) -> FuncListMap:
    """
    The dispatchers of the class and of its subclasses need the fallbacks
    this class body declared itself. A name may hold an instance bound
    fallback and a class bound one together, so each name has a list.

    Returns
    -------

    FuncListMap
      A 'dict[str, list[Callable]]', in declaration order.
    """
    return maybe(self.__fallback_map__, dict())

  def _getDeclaredFallbacks(self, name: str) -> list:
    """
    A name the body declared no fallback at has none, which needs an
    answer of its own beside the names that have.

    Returns
    -------

    list
      The fallbacks the body declared at the name, in declaration order,
      or an empty list when it declared none.
    """
    try:
      declared = self.getFallbacks()[name]
    except KeyError:
      #  This branch is reached by the following:
      #  - The body declared no fallback at the name
      return []
    else:
      return declared

  def getFinalizers(self, ) -> FuncMap:
    """
    The finalizers this class body declared itself, by name.

    Returns
    -------

    FuncMap
      A 'dict[str, Callable]'.
    """
    return maybe(self.__finalizer_map__, dict())

  def getMethodKinds(self) -> dict[str, tuple]:
    """
    The dispatchers of the class and of its subclasses need the kinds of
    method this class body declared each overloaded name as.

    Returns
    -------

    dict[str, tuple]
      From each name to the kinds declared at it, in the order first
      declared, each 'classmethod', 'staticmethod', or 'None' for an
      instance method.
    """
    return maybe(self.__method_kinds__, dict())

  def getFunctionKinds(self) -> dict[str, list]:
    """
    One name may hold bound methods, classmethods and staticmethods, so
    the dispatchers built for it need the kind of each function.

    Returns
    -------

    dict[str, list]
      From each name to a 'list[tuple[Callable, Any]]' of each function
      this class body declared at it, as the body handed it over, with
      its kind: 'classmethod', 'staticmethod', or 'None' for an instance
      method.
    """
    return maybe(self.__function_kinds__, dict())

  def _getDeclaredKind(self, name: str) -> tuple:
    """
    'None' is the kind of an instance method, so whether this body declared
    the name at all needs an answer of its own.

    Returns
    -------

    tuple
      The kinds the body declared the name as, in the order first
      declared, or an empty tuple when it declared nothing at the name.
    """
    kinds = self.getMethodKinds()
    try:
      declared = kinds[name]
    except KeyError:
      return ()
    else:
      return declared

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
      The kinds the nearer classes declare, or an empty tuple when none
      of them declares the name.

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
    if not kind or not found:
      return False
    for one in found:
      if any(one is other for other in kind):
        #  This branch is reached by the following:
        #  - The class declares the name as a kind the nearer classes
        #    declare as well
        return False
    return True

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
      kind = self._joinKinds(kind, space._getDeclaredKind(name))
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
  def _joinKinds(first: tuple, second: tuple) -> tuple:
    out = [*first]
    for kind in second:
      if not any(kind is other for other in out):
        out.append(kind)
    return (*out,)

  @staticmethod
  def _mayMeet(first: Any, second: Any) -> bool:
    """
    Two functions of one signature at a name leave dispatch undecided only
    if one call can reach both. A bound method is reached through an
    instance and a staticmethod through the class, so those two never
    meet; a classmethod is reached both ways and meets either.

    Parameters
    ----------

    first : Any
      The kind of one function: 'classmethod', 'staticmethod', or 'None'
      for an instance method.

    second : Any
      The kind of the other.

    Returns
    -------

    bool
      Whether one call can reach functions of both kinds.
    """
    kinds = (first, second)
    bound = any(kind is None for kind in kinds)
    static = any(kind is staticmethod for kind in kinds)
    return False if bound and static else True

  @staticmethod
  def _kindIn(kinds: list, func: Any) -> Any:
    """
    The kind of a function is looked up among the recorded ones by
    identity; one recorded nowhere is an instance method, as a function
    registered by hand is.

    Parameters
    ----------

    kinds : list
      A 'list[tuple[Callable, Any]]' of functions with their kinds.

    func : Any
      The function asked about.

    Returns
    -------

    Any
      'classmethod', 'staticmethod', or 'None' for an instance method.
    """
    for held, kind in kinds:
      if held is func:
        return kind
    return None

  def _mergeSigFuncs(
      self,
      collected: CollectedList,
      more: SigFuncList,
      distance: int,
      kinds: list,
  ) -> None:
    for sig, func in more:
      own = self._kindIn(kinds, func)
      for existing, held, __ in collected:
        if existing != sig:
          continue
        if self._mayMeet(self._kindIn(kinds, held), own):
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
    kinds = self._gatherFunctionKinds(spaces, name)
    for distance, space in enumerate(spaces):
      sigFuncs = space.getOverloads().get(name, [])
      self._mergeSigFuncs(out, sigFuncs, distance, kinds)
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
    kinds = self._gatherFunctionKinds(spaces, name)
    for distance, space in enumerate(spaces):
      sigFuncs = space.getVariadics().get(name, [])
      self._mergeSigFuncs(out, sigFuncs, distance, kinds)
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
    kinds = self._gatherFunctionKinds(spaces, name)
    for distance, space in enumerate(spaces):
      for sig, func in space.getFlexes().get(name, []):
        bag = sig.getBag()
        own = self._kindIn(kinds, func)
        for existing, held, __ in out:
          if existing.getBag() != bag:
            continue
          if self._mayMeet(self._kindIn(kinds, held), own):
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

  @staticmethod
  def _gatherFunctionKinds(spaces: tuple, name: str) -> list:
    out = []
    for space in spaces:
      try:
        recorded = space.getFunctionKinds()[name]
      except KeyError:
        #  This branch is reached by the following:
        #  - The class body recorded no kind at the name, as one whose
        #    declarations were registered by hand
        continue
      out.extend(recorded)
    return out

  def collectFunctionKinds(self, name: str) -> list:
    """
    The dispatchers of a name are built by the kind of each function, its
    own and the inherited ones: the bound methods are reached through an
    instance, the staticmethods through the class and the classmethods
    both ways.

    Implementation
    --------------

    The body and the namespaces from '_getInheritedSpaces' are asked in
    order.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    list
      A 'list[tuple[Callable, Any]]' of each function recorded at the
      name with its kind, nearest class first.
    """
    spaces = (self, *self._getInheritedSpaces(name))
    return self._gatherFunctionKinds(spaces, name)

  def collectFallback(self, name: str) -> Optional[Callable]:
    """
    The fallbacks of a name begin with that of the nearest class
    declaring one, up to the first plain definition, and a namespace class
    of a project may hand out a fallback of its own for a name by
    reimplementing this method.

    Implementation
    --------------

    The body and the namespaces from '_getInheritedSpaces' are asked in
    order, and the fallback the first of them declared first is returned.
    'collectFallbacks' begins with it and adds the instance bound or the
    class bound fallback the name still lacks, when one is declared.

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
      for fallback in space._getDeclaredFallbacks(name):
        return fallback
    return None

  def collectFallbacks(self, name: str) -> list:
    """
    A name holding bound methods beside staticmethods is reached two
    ways, through an instance and through the class, and a call nothing
    accepts may need a fallback either way. The fallbacks of a name are
    therefore two, apart: the instance bound fallback, for the calls
    through an instance, and the class bound fallback, for the calls
    through the class. A fallback declared as a bound method is instance
    bound and one declared as a staticmethod is class bound, so the two
    never answer one call and a name may hold both; one declared as a
    classmethod is both, and stands alone. A subclass may add the one its
    bases lack, and a fallback it declares replaces an inherited one that
    the same call could reach. A namespace class of a project that hands
    out a fallback of its own by reimplementing 'collectFallback' must
    still be asked.

    Implementation
    --------------

    The fallback 'collectFallback' gives comes first. The fallbacks of
    the body and of the namespaces from '_getInheritedSpaces' follow in
    order, each kept unless one call can reach both it and a fallback
    gathered already, as '_mayMeet' tells by their kinds. The kinds are
    those 'collectFunctionKinds' gives, where a function recorded nowhere
    is a bound method.

    Parameters
    ----------

    name : str
      The name.

    Returns
    -------

    list
      The fallbacks of the name, nearest first: none, one, or the
      instance bound fallback and the class bound one.
    """
    out = []
    nearest = self.collectFallback(name)
    if nearest is not None:
      out.append(nearest)
    kinds = self.collectFunctionKinds(name)
    for space in (self, *self._getInheritedSpaces(name)):
      for fallback in space._getDeclaredFallbacks(name):
        own = self._kindIn(kinds, fallback)
        for held in out:
          if self._mayMeet(self._kindIn(kinds, held), own):
            break
        else:
          out.append(fallback)
    return out

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
      flexible declaration of the same classes is, unless the two are a
      bound method and a staticmethod, which no call reaches together.
    """
    kinds = self._gatherFunctionKinds((self,), name)
    own = self._kindIn(kinds, func)
    bag = sig.getBag()
    for flexSig, flexFunc in self.getFlexes().get(name, []):
      if flexSig.getBag() != bag or flexFunc is func:
        continue
      if self._mayMeet(self._kindIn(kinds, flexFunc), own):
        raise DuplicateSignature(sig, flexFunc, func)
    existing = self.getOverloads()
    sigFuncs = existing.get(name, [])
    for oldSig, oldFunc in sigFuncs:
      if oldSig != sig:
        continue
      if oldFunc is func:
        break
      if self._mayMeet(self._kindIn(kinds, oldFunc), own):
        raise DuplicateSignature(sig, oldFunc, func)
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
      as one order, unless the two are a bound method and a staticmethod,
      which no call reaches together.
    """
    kinds = self._gatherFunctionKinds((self,), name)
    own = self._kindIn(kinds, func)
    bag = sig.getBag()
    for oldSig, oldFunc in self.getOverloads().get(name, []):
      if oldSig.getBag() != bag or oldFunc is func:
        continue
      if self._mayMeet(self._kindIn(kinds, oldFunc), own):
        raise DuplicateSignature(sig, oldFunc, func)
    existing = self.getFlexes()
    flexes = existing.get(name, [])
    for oldSig, oldFunc in flexes:
      if oldSig.getBag() != bag:
        continue
      if oldFunc is func:
        break
      if self._mayMeet(self._kindIn(kinds, oldFunc), own):
        raise DuplicateSignature(sig, oldFunc, func)
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
      An equal signature is declared for a different function, unless the
      two are a bound method and a staticmethod, which no call reaches
      together.
    """
    kinds = self._gatherFunctionKinds((self,), name)
    own = self._kindIn(kinds, func)
    existing = self.getVariadics()
    sigFuncs = existing.get(name, [])
    for oldSig, oldFunc in sigFuncs:
      if oldSig != sig:
        continue
      if oldFunc is func:
        break
      if self._mayMeet(self._kindIn(kinds, oldFunc), own):
        raise DuplicateSignature(sig, oldFunc, func)
    else:
      sigFuncs.append((sig, func,))
    existing[name] = sigFuncs
    self.__variadic_overload_map__ = existing

  def addMethodKind(self, name: str, kind: Any) -> None:
    """
    One name may be declared as several kinds of method, and which kinds
    a body declares decides what the class inherits at the name: a base
    sharing no kind with the nearer classes is hidden.

    Parameters
    ----------

    name : str
      The name.

    kind : Any
      'classmethod', 'staticmethod', or 'None' for an instance method.
    """
    kinds = self.getMethodKinds()
    kinds[name] = self._joinKinds(self._getDeclaredKind(name), (kind,))
    self.__method_kinds__ = kinds

  def addFunctionKind(self, name: str, kind: Any, *funcs) -> None:
    """
    'LoadSpaceHook' records the kind of each function a body declares at
    an overloaded name, since the dispatchers of the name are built by
    kind.

    Implementation
    --------------

    Each function is recorded once, compared by identity, with the kind
    of its first record.

    Parameters
    ----------

    name : str
      The name.

    kind : Any
      'classmethod', 'staticmethod', or 'None' for an instance method.

    *funcs
      The functions as the body handed them over, a 'PermuterMethod' of
      a flexible declaration included.
    """
    existing = self.getFunctionKinds()
    try:
      recorded = existing[name]
    except KeyError:
      #  This branch is reached by the following:
      #  - The first function the body declares at the name
      recorded = []
    for func in funcs:
      if any(func is held for held, _ in recorded):
        continue
      recorded.append((func, kind))
    existing[name] = recorded
    self.__function_kinds__ = existing

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
    Two fallbacks at one name leave it undecided which takes a call
    nothing accepts, unless no call can reach both. A fallback declared
    as a bound method is the instance bound fallback of its name, reached
    through an instance, and one declared as a staticmethod the class
    bound fallback, reached through the class, so a body may declare
    those two at one name; one declared as a classmethod is both. A
    subclass may replace an inherited fallback, which is not on record
    here.

    Implementation
    --------------

    The kind of each function is the one 'addFunctionKind' recorded for
    it, which 'LoadSpaceHook' records before it registers the fallback; a
    function recorded nowhere is a bound method.

    Parameters
    ----------

    name : str
      The name.

    func : Callable
      The fallback.

    Raises
    ------

    DuplicateSignature
      The body declared a different fallback at the name already, unless
      the two are a bound method and a staticmethod, which no call
      reaches together.
    """
    kinds = self._gatherFunctionKinds((self,), name)
    own = self._kindIn(kinds, func)
    existing = self.getFallbacks()
    held = self._getDeclaredFallbacks(name)
    for oldFunc in held:
      if oldFunc is func:
        break
      if self._mayMeet(self._kindIn(kinds, oldFunc), own):
        raise DuplicateSignature('fallback', oldFunc, func)
    else:
      held.append(func)
    existing[name] = held
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
