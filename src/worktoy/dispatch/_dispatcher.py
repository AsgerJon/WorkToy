"""
Dispatcher maps type signatures to functions and resolves overloaded
calls to the matching one.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from collections import Counter
from functools import wraps
from types import FunctionType as Func
from types import MethodType
from typing import TYPE_CHECKING

from ..core import Object
from ..utilities import maybe, typeCast, textFmt, bipartiteMatching
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import ReadOnlyError, ProtectedError, WriteOnceError
from ..waitaminute.dispatch import DispatchException, DuplicateSignature
from ..waitaminute.dispatch import TypeCastException
from . import TypeSig, PermuterMethod, CallMeMaybe

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Never, TypeAlias, Optional, Self
  from . import Dispatcher

  Method: TypeAlias = Callable[[Any, ...], Any]
  SigFuncList: TypeAlias = list[tuple[TypeSig, Method]]
  SigFuncMap: TypeAlias = dict[TypeSig, Method]


def _dropReceiver(func: Method) -> Method:
  """
  The dispatch function passes a receiver ahead of the arguments of every
  call, the class for a dispatcher standing for a staticmethod, and a
  staticmethod takes none. Each function of such a dispatcher must
  receive the arguments alone, and must still show its own name and
  docstring.

  Implementation
  --------------

  The wrapper takes the receiver by position and calls the function
  without it; 'functools.wraps' copies the name, docstring and
  attributes.

  Parameters
  ----------

  func : Method
    A 'Callable[..., Any]' taking the arguments of the call alone.

  Returns
  -------

  Method
    A function taking the receiver first and dropping it.
  """

  @wraps(func)
  def dropped(receiver: Any, *args, **kwargs) -> Any:
    return func(*args, **kwargs)

  return dropped


def _uniformType(types: tuple) -> Optional[type]:
  first = types[0]
  for type_ in types:
    if type_ is not first:
      return None
  return first


#  A flexible declaration of at most this many classes is registered as one
#  concrete signature per order of its classes. The orders number the
#  factorial of the classes, so a longer declaration is registered once and
#  matched by its classes in any order.
_MAX_EXPANDED_FLEX: int = 3


def _orderByClass(declared: tuple, args: tuple) -> tuple:
  #  Each declared position takes the next argument of its exact class, in
  #  the order the caller gave them.
  queues = dict()
  for arg in args:
    try:
      queues[type(arg)].append(arg)
    except KeyError:
      queues[type(arg)] = [arg]
  iterators = {key: iter(queue) for key, queue in queues.items()}
  return (*(next(iterators[type_]) for type_ in declared),)


def _orderByInstance(declared: tuple, args: tuple) -> Optional[tuple]:
  if len(args) != len(declared):
    return None
  slots = [
    (*(i for i, arg in enumerate(args) if isinstance(arg, type_)),)
    for type_ in declared
  ]
  try:
    order = bipartiteMatching(slots)
  except ValueError:
    return None
  return (*(args[i] for i in order),)


#  The builtin number classes, each narrower than those after it.
_NUMBERS: tuple = (bool, int, float, complex)


def _castWidening(type_: type, arg: Any) -> Any:
  """
  'typeCast' turns a whole 'float' such as '2.0' into an 'int', so where
  every cast is allowed, an 'int' parameter and a 'float' parameter both
  take '2.0' and '7', and the first signature found decides which goes
  where: a flexible declaration of an 'int' and a 'float' then hands the
  float to the 'int' parameter and the int to the 'float' one. A cast
  tried before that one must cast a number only to a wider number, never
  to a narrower one, and cast everything else as 'typeCast' does.

  Implementation
  --------------

  An instance of 'type_' is returned as it is. A class other than the
  builtin number classes is left to 'typeCast'. A number class takes,
  through 'typeCast', only a value of a number class before it in
  '_NUMBERS': a 'float' an 'int', a 'complex' an 'int' or a 'float', and
  an 'int' or a 'bool' nothing it is not already.

  Parameters
  ----------

  type_ : type
    The class of the position.

  arg : Any
    The argument.

  Returns
  -------

  Any
    The argument, or its cast.

  Raises
  ------

  TypeCastException
    The cast would narrow a number, or 'typeCast' refuses it.
  """
  if isinstance(arg, type_):
    return arg
  if type_ not in _NUMBERS:
    return typeCast(type_, arg)
  for narrower in _NUMBERS[:_NUMBERS.index(type_)]:
    if isinstance(arg, narrower):
      return typeCast(type_, arg)
  raise TypeCastException(type_, arg)


def _orderByCast(
    declared: tuple,
    args: tuple,
    cast: Callable,
) -> Optional[tuple]:
  if len(args) != len(declared):
    return None
  values, slots = dict(), []
  for position, type_ in enumerate(declared):
    fitting = []
    for i, arg in enumerate(args):
      try:
        values[position, i] = cast(type_, arg)
      except (ValueError, TypeError):
        continue
      fitting.append(i)
    slots.append((*fitting,))
  try:
    order = bipartiteMatching(slots)
  except ValueError:
    return None
  return (*(values[position, i] for position, i in enumerate(order)),)


class Dispatcher(Object):
  """
  A method declared several times with '@overload', once per signature,
  needs one callable at its name that picks the declaration matching the
  positional arguments of each call. Most calls pass exactly the declared
  classes, and those must cost no more than a dictionary lookup. A call
  passing a subclass must still find its declaration, and one passing a
  value that converts without loss, as an 'int' for a 'float', may too.
  A subclass overloading a name it inherits must win the calls its own
  declarations accept, and leave the rest to the inherited ones. A call
  nothing accepts must fail with an error listing what was received and
  what is declared, unless a fallback takes it, and a finalizer may need
  to run after every call. An overloaded name may be a classmethod or a
  staticmethod as well, and must then receive the class, or nothing
  before the arguments, as such a method does.

  Implementation
  --------------

  The namespace of a class whose metaclass is based on 'BaseMeta' builds
  the dispatcher of each overloaded name, and registers the declarations
  of the class body and those the class inherits before the class is
  created. Registrations are kept in lists, each with its distance: 0 for
  the class itself, 1 for the nearest class it inherits from, and so on.
  The first read compiles them into a dispatch function, which tries, in
  order:

  1. Exact classes: one lookup of the classes of the call, as a plain
     tuple; one of the classes of the call in any order, for a flexible
     declaration of more than three classes; and one per distinct prefix
     length of the variadic signatures, keyed by the prefix and the one
     class all trailing arguments share. A hit from a farther class first
     lets the nearer classes answer through 'isinstance'.
  2. 'isinstance', class by class, nearest first; within a class the
     concrete signatures in registration order, then the flexible
     declarations of more than three classes, then the variadic
     signatures, most recent first.
  3. A cast of each argument that is not an instance, where a number
     class takes only a narrower number, 'int' to 'float' to 'complex',
     and every other class casts as 'typeCast' allows; farthest class
     first, so a subclass never redirects a call its parent handled
     through such a cast: the concrete signatures, the flexible
     declarations, then the variadic signatures.
  4. The same with every cast 'typeCast' allows, narrowing included, as
     '2.0' to the 'int' '2'.
  5. The fallback, if any, else 'DispatchException'.

  A flexible declaration of up to three classes is registered as one
  concrete signature per order. A longer one is registered once. Found by
  exact classes, each declared position takes the next argument of its
  class in the order the caller gave them; in the 'isinstance' and cast
  passes, 'bipartiteMatching' gives each argument a position it fits.

  Tier 3 comes before tier 4 so that a flexible declaration keeps each
  number in its role. With every cast allowed, '2.0' and '7' both fit an
  'int' and a 'float' parameter, and the first signature found would
  decide which goes where; with numbers widened only, '2.0' fits the
  'float' parameter alone. A subclass taking a call in tier 3 therefore
  wins over a base that would take it only in tier 4.

  The finalizer runs in a 'finally' block. Keywords play no part in
  matching and pass to the selected function. Within one class, the
  first registered signature accepting a call wins passes 2 and 3; the
  dispatcher does not rank signatures by how specific they are, so the
  more specific one is registered first. Read through the class, a
  'Dispatcher' gives the dispatch function; through an instance, a bound
  method of it; the dispatcher itself is in 'Owner.__dict__'.
  'setMethodKind', before anything is registered, makes a dispatcher a
  classmethod or a staticmethod. Either is bound to the class at every
  read, through the class or an instance, and the class is the receiver
  the dispatch function passes on; a staticmethod registers each
  function, the fallback and the finalizer behind '_dropReceiver', and a
  'PermuterMethod' over the wrapped function.

  Attributes
  ----------

  __no_this_reference__ : bool
    'True'. 'THIS[Parent].name' reads it off the class of what the name
    holds and refuses a reference to an overloaded method with
    'OverloadReference', since the clone it would take replaces the
    dispatcher the namespace of the subclass builds.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __no_this_reference__ = True

  #  Private Variables
  __sig_funcs__ = None
  __sig_distances__ = None
  __variadic_funcs__ = None
  __variadic_distances__ = None
  __flex_funcs__ = None
  __flex_distances__ = None
  __fallback_func__ = None
  __field_name__ = None
  __field_owner__ = None
  __finalizer_func__ = None
  __compiled_func__ = None
  #  'classmethod', 'staticmethod', or 'None' for an instance method.
  __method_kind__ = None
  #  The '_dropReceiver' wrapper of each function, for a staticmethod.
  __static_adapters__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getSigFuncList(self) -> SigFuncList:
    return maybe(self.__sig_funcs__, [])

  def _getSigFuncMap(self) -> SigFuncMap:
    return {sig: func for sig, func in self._getSigFuncList()}

  def _getVariadicFuncs(self) -> SigFuncList:
    return maybe(self.__variadic_funcs__, [])

  def _getSigDistances(self) -> list[int]:
    return maybe(self.__sig_distances__, [])

  def _getVariadicDistances(self) -> list[int]:
    return maybe(self.__variadic_distances__, [])

  def _getFlexFuncs(self) -> SigFuncList:
    return maybe(self.__flex_funcs__, [])

  def _getFlexDistances(self) -> list[int]:
    return maybe(self.__flex_distances__, [])

  def _getDeclaredSigs(self) -> list[TypeSig]:
    out = [sig for sig, _ in self._getSigFuncList()]
    out += [sig for sig, _ in self._getFlexFuncs()]
    out += [sig for sig, _ in self._getVariadicFuncs()]
    return out

  def _getExactFlexes(self) -> dict:
    out = dict()
    flexFuncs = self._getFlexFuncs()
    for (sig, func), distance in zip(flexFuncs, self._getFlexDistances()):
      out[sig.getBag()] = (distance, sig.getRawTypes(), func)
    return out

  @staticmethod
  def _coversExactly(sig: TypeSig, types: tuple) -> bool:
    raw = sig.getRawTypes()
    prefix, inner = raw[:-1], raw[-1].__inner_type__
    if len(types) < len(prefix):
      return False
    for this, that in zip(types, prefix):
      if this is not that:
        return False
    for type_ in types[len(prefix):]:
      if type_ is not inner:
        return False
    return True

  def _getExactEntries(self) -> dict[tuple, tuple[int, Method]]:
    """
    A call passing exactly the classes of a concrete signature must reach
    the nearest class that accepts it, at the cost of one lookup. When a
    subclass declares a variadic signature that accepts the same call by
    exact class, the subclass wins it, while a variadic signature of the
    same class never displaces an explicit one.

    Implementation
    --------------

    The classes of each concrete signature, as a plain tuple, map to its
    own registration, unless a variadic signature of a strictly nearer
    class covers it exactly; the nearest such class wins, and within it
    the most recent declaration. A tuple hashes as the signature does,
    and compares its classes by identity, since neither 'type' nor
    'AbstractMetaclass' defines '__eq__', in C rather than through the
    methods of 'TypeSig'.

    Returns
    -------

    dict[tuple, tuple[int, Method]]
      For the classes of each concrete signature, the distance and the
      function of the winning registration.
    """
    variadicFuncs = self._getVariadicFuncs()
    variadics = [*zip(variadicFuncs, self._getVariadicDistances())]
    out = dict()
    sigFuncs = self._getSigFuncList()
    for (sig, func), distance in zip(sigFuncs, self._getSigDistances()):
      types = sig.getRawTypes()
      best = None
      for index, ((variadic, nearerFunc), nearerDistance) in enumerate(
          variadics
      ):
        if nearerDistance >= distance:
          continue
        if not self._coversExactly(variadic, types):
          continue
        #  Nearest class first, and within a class the most recent
        #  declaration, the rank '_getExactVariadics' gives.
        rank = (nearerDistance, -index)
        if best is None or rank < best[0]:
          best = (rank, nearerFunc)
      if best is None:
        out[types] = (distance, func)
      else:
        out[types] = (best[0][0], best[1])
    return out

  def _getExactVariadics(self) -> tuple[dict, dict, tuple[int, ...]]:
    """
    A call matching a variadic signature by exact class must be found by
    lookup too, not by trying every variadic signature in turn, and of
    several accepting one call the most recent declaration of the nearest
    class must win.

    Implementation
    --------------

    One table is keyed by prefix length, prefix classes and inner class,
    for calls with trailing arguments; another by prefix length and prefix
    classes alone, for calls of the bare prefix. Each entry keeps the best
    rank, distance first and then declaration order reversed.

    Returns
    -------

    tuple[dict, dict, tuple[int, ...]]
      The two tables and the distinct prefix lengths, ascending.
    """
    tailed, empty, lengths = dict(), dict(), []
    distances = self._getVariadicDistances()
    for index, (sig, func) in enumerate(self._getVariadicFuncs()):
      raw = sig.getRawTypes()
      prefix, inner = raw[:-1], raw[-1].__inner_type__
      prefixLen = len(prefix)
      #  Nearest class first, and within a class the most recent
      #  declaration, so a later declaration takes a call an earlier one
      #  accepts as well.
      rank = (distances[index], -index)
      for table, key in (
          (tailed, (prefixLen, prefix, inner)),
          (empty, (prefixLen, prefix)),
      ):
        held = table.get(key)
        if held is None or rank < held[0]:
          table[key] = (rank, func)
      if prefixLen not in lengths:
        lengths.append(prefixLen)
    return tailed, empty, (*sorted(lengths),)

  @staticmethod
  def _getCastOrder(
      sigFuncs: SigFuncList,
      distances: list[int],
  ) -> SigFuncList:
    """
    Adding a signature in a subclass must never redirect a call its parent
    already handled through a cast of the same tier.

    Implementation
    --------------

    The registrations are sorted farthest first, keeping registration
    order among equal distances.

    Parameters
    ----------

    sigFuncs : SigFuncList
      A 'list[tuple[TypeSig, Method]]' in registration order.

    distances : list[int]
      The distance of each registration.

    Returns
    -------

    SigFuncList
      The same pairs in the order the cast pass tries them.
    """
    positions = sorted(range(len(sigFuncs)), key=lambda i: -distances[i])
    return [sigFuncs[i] for i in positions]

  def _getVariadicOrder(self, nearestFirst: bool) -> SigFuncList:
    """
    Of several variadic signatures of one class accepting a call, the most
    recent declaration must win, in the 'isinstance' pass nearest class
    first and in the cast pass farthest first.

    Parameters
    ----------

    nearestFirst : bool
      'True' for the 'isinstance' pass, 'False' for the cast pass.

    Returns
    -------

    SigFuncList
      A 'list[tuple[TypeSig, Method]]' in that order.
    """
    pairs = self._getVariadicFuncs()
    distances = self._getVariadicDistances()
    sign = 1 if nearestFirst else -1
    positions = sorted(
        range(len(pairs)), key=lambda i: (sign * distances[i], -i),
    )
    return [pairs[i] for i in positions]

  def _getMatchTiers(
      self,
  ) -> list[tuple[int, SigFuncList, SigFuncList, SigFuncList]]:
    """
    In the 'isinstance' pass, a registration of a nearer class must take
    every call it accepts before any of a farther class is asked.

    Implementation
    --------------

    The registrations are grouped by distance, nearest first; within a
    group, the concrete ones in registration order, then the flexible
    declarations of more than three classes in registration order, then
    the variadic ones most recent first.

    Returns
    -------

    list[tuple[int, SigFuncList, SigFuncList, SigFuncList]]
      The distance, the concrete pairs, the flexible pairs and the
      variadic pairs of each group.
    """
    concretes, flexes, variadics = dict(), dict(), dict()
    sigFuncs = self._getSigFuncList()
    for (sig, func), distance in zip(sigFuncs, self._getSigDistances()):
      concretes.setdefault(distance, []).append((sig, func))
    flexFuncs = self._getFlexFuncs()
    for (sig, func), distance in zip(flexFuncs, self._getFlexDistances()):
      flexes.setdefault(distance, []).append((sig, func))
    variadicFuncs = self._getVariadicFuncs()
    variadicDistances = self._getVariadicDistances()
    for index in reversed(range(len(variadicFuncs))):
      group = variadics.setdefault(variadicDistances[index], [])
      group.append(variadicFuncs[index])
    out = []
    for distance in sorted({*concretes, *flexes, *variadics}):
      group = (
        concretes.get(distance, []),
        flexes.get(distance, []),
        variadics.get(distance, []),
      )
      out.append((distance, *group))
    return out

  def _getFallbackFunction(self) -> Optional[Method]:
    return self.__fallback_func__

  def _getFinalizerFunction(self) -> Optional[Method]:
    return self.__finalizer_func__

  def getMethodKind(self) -> Any:
    """
    Code holding a dispatcher may need to know which kind of method it
    stands for.

    Returns
    -------

    Any
      'classmethod' or 'staticmethod', or 'None' for an instance method.
    """
    return self.__method_kind__

  def _hasRegistrations(self) -> bool:
    registries = (
      self._getSigFuncList(),
      self._getFlexFuncs(),
      self._getVariadicFuncs(),
    )
    roles = (self.__fallback_func__, self.__finalizer_func__)
    if any(registries):
      return True
    return True if any(role is not None for role in roles) else False

  def _getFieldName(self, ) -> str:
    fieldName = self.__field_name__
    if fieldName is None:
      raise MissingVariable(self, '__field_name__', str)
    return fieldName

  def _getFieldOwner(self, ) -> type:
    fieldOwner = self.__field_owner__
    if fieldOwner is None:
      raise MissingVariable(self, '__field_owner__', type)
    return fieldOwner

  def _createCachedFunction(self) -> None:
    """
    Dispatch runs on every call of an overloaded method, so the work of
    ordering the registrations must happen once, not per call, and the
    callable at the name must look like the method a reader wrote: its
    name, qualified name, file and docstring.

    Implementation
    --------------

    The tables of every pass are taken now and closed over by the dispatch
    function, which is cached; any registration afterwards clears the
    cache. The dispatch function takes the instance by position, so no
    keyword of a call collides with a parameter of its own. It takes the
    classes of the arguments once, as a plain tuple, the key of every
    exact table, and builds no 'TypeSig'; only 'DispatchException' builds
    one, for its message. Its docstring is that of
    '_getDocumentedFunction'.

    Raises
    ------

    MissingVariable
      The dispatcher has not been placed in a class.
    """
    exactEntries = self._getExactEntries()
    exactFlexes = self._getExactFlexes()
    tailed, empty, prefixLens = self._getExactVariadics()
    tiers = self._getMatchTiers()
    nearest = tiers[0][0] if tiers else 0
    castFuncs = self._getCastOrder(
        self._getSigFuncList(), self._getSigDistances(),
    )
    castFlexes = self._getCastOrder(
        self._getFlexFuncs(), self._getFlexDistances(),
    )
    castVariadics = self._getVariadicOrder(False)
    fallback = self._getFallbackFunction()
    finalizer = self._getFinalizerFunction()
    dispatcher = self
    fieldName = self._getFieldName()
    owner = self._getFieldOwner()

    def exactVariadic(argTypes: tuple) -> Optional[tuple[int, Method]]:
      """The distance and the function of the variadic signature accepting
      the call of 'argTypes' by exact type, the most recent of the nearest
      class among those that do, or None when none does."""
      best = None
      for prefixLen in prefixLens:
        if len(argTypes) < prefixLen:
          break
        prefix, tail = argTypes[:prefixLen], argTypes[prefixLen:]
        if tail:
          inner = _uniformType(tail)
          key = (prefixLen, prefix, inner)
          hit = None if inner is None else tailed.get(key)
        else:
          hit = empty.get((prefixLen, prefix))
        if hit is not None and (best is None or hit[0] < best[0]):
          best = hit
      if best is None:
        return None
      (distance, _), func = best
      return distance, func

    def exactLoose(argTypes: tuple, args: tuple) -> Optional[tuple]:
      """The distance, the function and the arguments in declared order of
      the flexible declaration or the variadic signature accepting the call
      of 'argTypes' by exact type, the nearer of the two, the flexible one
      when both are of one class, or None when neither does."""
      flexHit = None
      if exactFlexes:
        #  The bag 'TypeSig.getBag' gives, from the classes of the call.
        bag = frozenset(Counter(argTypes).items())
        try:
          distance, declared, func = exactFlexes[bag]
        except KeyError:
          flexHit = None
        else:
          flexHit = distance, func, _orderByClass(declared, args)
      variadicHit = exactVariadic(argTypes) if prefixLens else None
      if variadicHit is None:
        return flexHit
      if flexHit is None or variadicHit[0] < flexHit[0]:
        return (*variadicHit, args)
      return flexHit

    def matchInstances(args: tuple, before: Optional[int], ) -> Any:
      """The function, and the arguments in the order it takes them, of
      the registration accepting 'args' through 'isinstance', nearest class
      first, asking only the classes nearer than the distance 'before' when
      it is given; within a class the concrete signatures in registration
      order, then the flexible declarations, then the variadic ones, the
      most recent first. None when none accepts the call."""
      for distance, concretes, flexes, variadics in tiers:
        if before is not None and distance >= before:
          return None
        for sig, func in concretes:
          if len(args) != len(sig):
            continue
          for arg, type_ in zip(args, sig):
            if not isinstance(arg, type_):
              break
          else:
            return func, args
        for sig, func in flexes:
          ordered = _orderByInstance(sig.getRawTypes(), args)
          if ordered is not None:
            return func, ordered
        for sig, func in variadics:
          rawTypes = sig.getRawTypes()
          prefix = rawTypes[:-1]
          innerType = rawTypes[-1].__inner_type__
          if len(args) < len(prefix):
            continue
          matched = True
          for arg, type_ in zip(args[:len(prefix)], prefix):
            if not isinstance(arg, type_):
              matched = False
              break
          if not matched:
            continue
          for arg in args[len(prefix):]:
            if not isinstance(arg, innerType):
              matched = False
              break
          if matched:
            return func, args
      return None

    def matchCasts(args: tuple, cast: Callable) -> Any:
      """The function, and the arguments in the order it takes them, of
      the registration accepting 'args' when 'cast' is applied to each
      argument that is not an instance, farthest class first; within a
      class the concrete signatures in registration order, then the
      flexible declarations, then the variadic ones, the most recent
      first. None when none accepts the call."""
      for sig, func in castFuncs:
        if len(args) != len(sig):
          continue
        castArgs = []
        for arg, type_ in zip(args, sig):
          if isinstance(arg, type_):
            castArgs.append(arg)
            continue
          try:
            castedArg = cast(type_, arg)
          except (ValueError, TypeError):
            break
          else:
            castArgs.append(castedArg)
        else:
          return func, castArgs
      for sig, func in castFlexes:
        castArgs = _orderByCast(sig.getRawTypes(), args, cast)
        if castArgs is not None:
          return func, castArgs
      for sig, func in castVariadics:
        rawTypes = sig.getRawTypes()
        prefix = rawTypes[:-1]
        innerType = rawTypes[-1].__inner_type__
        if len(args) < len(prefix):
          continue
        castArgs = []
        matched = True
        for arg, type_ in zip(args[:len(prefix)], prefix):
          if isinstance(arg, type_):
            castArgs.append(arg)
            continue
          try:
            castArgs.append(cast(type_, arg))
          except (ValueError, TypeError):
            matched = False
            break
        if not matched:
          continue
        for arg in args[len(prefix):]:
          if isinstance(arg, innerType):
            castArgs.append(arg)
            continue
          try:
            castArgs.append(cast(innerType, arg))
          except (ValueError, TypeError):
            matched = False
            break
        if matched:
          return func, castArgs
      return None

    def dispatch(*args, **kwargs) -> Any:
      #  The instance is taken from 'args' by position rather than named
      #  as a parameter, so a keyword of the caller named 'instance' goes
      #  through to the function the call selects.
      if not args:
        infoSpec = """%s.%s() missing 1 required positional argument:
        'self'"""
        raise TypeError(textFmt(infoSpec % (owner.__name__, fieldName)))
      instance, args = args[0], args[1:]
      #  The exception of the call itself, for the finalizer to chain
      #  from. 'sys.exc_info' would also report an exception the caller
      #  is handling, when the call raised nothing.
      raised = None
      try:
        argTypes = (*map(type, args),)
        try:
          hit = exactEntries.get(argTypes, None)
          if hit is None:
            hit = exactLoose(argTypes, args)
          else:
            hit = (*hit, args)
        except TypeError:
          #  An argument whose class cannot be hashed misses the exact-type
          #  lookups and goes on to the 'isinstance' passes.
          hit = None
        #  FASTEST, unless a nearer class accepts the call through
        #  'isinstance': the match of the nearer class wins either way.
        if hit is not None:
          distance, func, callArgs = hit
          if distance > nearest:
            nearer = matchInstances(args, distance)
            if nearer is not None:
              func, callArgs = nearer
          return func(instance, *callArgs, **kwargs)
        #  FAST, nearest class first
        found = matchInstances(args, None)
        if found is not None:
          func, callArgs = found
          return func(instance, *callArgs, **kwargs)
        #  SLOW, numbers widened only
        found = matchCasts(args, _castWidening)
        if found is not None:
          func, callArgs = found
          return func(instance, *callArgs, **kwargs)
        #  SLOWER, every cast 'typeCast' allows
        found = matchCasts(args, typeCast)
        if found is not None:
          func, callArgs = found
          return func(instance, *callArgs, **kwargs)
        #  FALLBACK
        if callable(fallback):
          return fallback(instance, *args, **kwargs)
        raise DispatchException(dispatcher, args, kwargs)
      except BaseException as callException:
        raised = callException
        raise
      finally:
        if callable(finalizer):
          try:
            finalizer(instance, *args, **kwargs)
          except Exception as finalException:
            if raised is None:
              raise finalException
            raise finalException from raised

    ownerName = owner.__name__
    dispatch.__name__ = fieldName
    dispatch.__qualname__ = '%s.%s' % (ownerName, fieldName)
    dispatch.__module__ = owner.__module__
    documented = self._getDocumentedFunction()
    if documented is None:
      #  This branch is reached by the following:
      #  - The dispatcher holds no function at all
      dispatch.__doc__ = None
    else:
      dispatch.__doc__ = documented.__doc__
    self.__compiled_func__ = dispatch

  def _getDocumentedFunction(self) -> Optional[Method]:
    """
    'help' on an overloaded method must show the docstring its author
    wrote.

    Implementation
    --------------

    The first concrete registration documents the dispatch, else the first
    flexible declaration of more than three classes, else the first
    variadic one, else the fallback, else the finalizer; a
    'PermuterMethod' is documented by the function it holds. Inherited
    registrations follow the class's own in the same lists, so a class
    declaring only variadic overloads at a name where it inherits
    concrete ones shows the inherited docstring.

    Returns
    -------

    Method or None
      The function whose docstring is shown.
    """
    for _, func in self._getSigFuncList():
      return self._unwrapCallMeMaybe(func)
    for _, func in self._getFlexFuncs():
      return self._unwrapCallMeMaybe(func)
    for _, func in self._getVariadicFuncs():
      return self._unwrapCallMeMaybe(func)
    fallback = self._getFallbackFunction()
    if fallback is not None:
      return self._unwrapCallMeMaybe(fallback)
    return self._unwrapCallMeMaybe(self._getFinalizerFunction())

  @staticmethod
  def _unwrapCallMeMaybe(func: Any) -> Any:
    if isinstance(func, CallMeMaybe):
      return func.__wrapped__
    return func

  def _getCachedFunction(self, **kwargs) -> Callable:
    if self.__compiled_func__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createCachedFunction()
      return self._getCachedFunction(_recursion=True)  # pragma: no mutate
    return self.__compiled_func__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setMethodKind(self, kind: Any) -> None:
    """
    A dispatcher must stand for a classmethod or a staticmethod as well as
    for an instance method. The kind decides what a read binds and how
    every function is registered, so it is set before anything is
    registered, and nothing but the three kinds is admitted.

    Implementation
    --------------

    The kind is recorded and the compiled dispatch function cleared.

    Parameters
    ----------

    kind : Any
      'classmethod', 'staticmethod', or 'None' for an instance method.

    Raises
    ------

    TypeError
      'kind' is not one of the three.

    WriteOnceError
      A function, a fallback or a finalizer is registered already.
    """
    kinds = (None, classmethod, staticmethod)
    if not any(kind is allowed for allowed in kinds):
      infoSpec = """The method kind of a dispatcher is 'classmethod',
      'staticmethod', or None for an instance method, not '%s'."""
      raise TypeError(textFmt(infoSpec % (kind,)))
    if self._hasRegistrations():
      raise WriteOnceError(self, self.__method_kind__, kind)
    self.__method_kind__ = kind
    self.__compiled_func__ = None

  def _adaptToKind(self, func: Method) -> Method:
    """
    The dispatch function passes a receiver ahead of the arguments of every
    call, and a staticmethod takes none, so each function of a dispatcher
    standing for a staticmethod must be called without it. A function
    registered under several signatures must still be one function to the
    checks comparing registrations.

    Implementation
    --------------

    For a staticmethod, a function is wrapped by '_dropReceiver', the
    wrapper kept in '__static_adapters__' under the function; a
    'PermuterMethod' is rebuilt over the wrapped function with the same
    arrangement, so it still reorders the arguments after the receiver.
    For the other kinds the function is returned as it is.

    Parameters
    ----------

    func : Method
      The function, or a 'PermuterMethod' of a flexible declaration.

    Returns
    -------

    Method
      What the dispatcher registers.
    """
    if self.__method_kind__ is not staticmethod:
      return func
    if isinstance(func, PermuterMethod):
      inner = self._adaptToKind(func.__wrapped__)
      return PermuterMethod(inner, func.arrangement)
    adapters = self.__static_adapters__
    if adapters is None:
      adapters = dict()
      self.__static_adapters__ = adapters
    try:
      adapted = adapters[func]
    except KeyError:
      #  This branch is reached by the following:
      #  - The first registration of the function on this dispatcher
      adapted = _dropReceiver(func)
      adapters[func] = adapted
    return adapted

  def addSigFunc(
      self,
      sig: TypeSig,
      func: Method,
      distance: int = 0,
  ) -> Method:
    """
    A dispatcher must accept registrations one concrete signature at a
    time, from its namespace as the class is created, and two functions at
    one signature would leave dispatch undecided.

    Implementation
    --------------

    The registration is appended with its distance, and the compiled
    dispatch function is cleared. Placing the dispatcher replaces 'THIS'
    in every signature registered before.

    Parameters
    ----------

    sig : TypeSig
      The signature, without a trailing 'ARGS'.

    func : Method
      A 'Callable[[Any, ...], Any]' taking the instance first.

    distance : int, optional
      How far from the owning class the registration comes. Defaults to 0.

    Returns
    -------

    Method
      'func' itself.

    Raises
    ------

    DuplicateSignature
      An equal signature is registered already, at any distance, or the
      signature is one order of a flexible declaration of another function
      at the same distance.
    """
    load = self._adaptToKind(func)
    existing = self._getSigFuncList()
    for existingSig, existingFunc in existing:
      if existingSig == sig:
        raise DuplicateSignature(sig, existingFunc, func)
    bag = sig.getBag()
    flexPairs = zip(self._getFlexFuncs(), self._getFlexDistances())
    for (flexSig, flexFunc), flexDistance in flexPairs:
      if flexDistance != distance or flexFunc is load:
        continue
      if flexSig.getBag() == bag:
        raise DuplicateSignature(sig, flexFunc, func)
    self.__sig_funcs__ = [*existing, (sig, load,)]
    self.__sig_distances__ = [*self._getSigDistances(), distance]
    self.__compiled_func__ = None
    return func

  def addFlexSigFunc(
      self,
      sig: TypeSig,
      func: Method,
      distance: int = 0,
  ) -> Method:
    """
    A flexible declaration of more than three classes has as many orders
    as the factorial of its classes, too many to register one signature
    each, so the dispatcher must accept it as one registration standing
    for every order, and refuse it where its classes are declared already.

    Implementation
    --------------

    As 'addSigFunc', with the signature in the declared order of its
    classes. Two declarations are the same when 'TypeSig.getBag' gives one
    value for both: an equal flexible declaration is refused at any
    distance, and a concrete signature of the same classes for another
    function at the same distance. A nearer class declaring one order
    explicitly takes that order and leaves the others to the inherited
    declaration, and one function declared under one order and flexibly
    takes that order as declared.

    Parameters
    ----------

    sig : TypeSig
      The signature, in the order the function takes its arguments.

    func : Method
      A 'Callable[[Any, ...], Any]' taking the instance first.

    distance : int, optional
      How far from the owning class the registration comes. Defaults to 0.

    Returns
    -------

    Method
      'func' itself.

    Raises
    ------

    DuplicateSignature
      A flexible declaration of the same classes is registered already, or
      a concrete signature of them for another function at the same
      distance.
    """
    load = self._adaptToKind(func)
    bag = sig.getBag()
    existing = self._getFlexFuncs()
    for existingSig, existingFunc in existing:
      if existingSig.getBag() == bag:
        raise DuplicateSignature(sig, existingFunc, func)
    sigPairs = zip(self._getSigFuncList(), self._getSigDistances())
    for (existingSig, existingFunc), existingDistance in sigPairs:
      if existingDistance != distance or existingFunc is load:
        continue
      if existingSig.getBag() == bag:
        raise DuplicateSignature(sig, existingFunc, func)
    self.__flex_funcs__ = [*existing, (sig, load,)]
    self.__flex_distances__ = [*self._getFlexDistances(), distance]
    self.__compiled_func__ = None
    return func

  def addVariadicSigFunc(
      self,
      sig: TypeSig,
      func: Method,
      distance: int = 0,
  ) -> Method:
    """
    A dispatcher must accept variadic registrations too. Several variadic
    signatures accepting one call are no conflict; the most recent of the
    nearest class takes it.

    Implementation
    --------------

    As 'addSigFunc', but repeats are appended rather than refused. That
    the signature ends in an 'ARGS' instance is not checked.

    Parameters
    ----------

    sig : TypeSig
      The signature, ending in an 'ARGS' instance.

    func : Method
      A 'Callable[[Any, ...], Any]' taking the instance first.

    distance : int, optional
      How far from the owning class the registration comes. Defaults to 0.

    Returns
    -------

    Method
      'func' itself.
    """
    existing = self._getVariadicFuncs()
    load = self._adaptToKind(func)
    self.__variadic_funcs__ = [*existing, (sig, load,)]
    self.__variadic_distances__ = [*self._getVariadicDistances(), distance]
    self.__compiled_func__ = None
    return func

  def setFallbackFunction(self, func: Method) -> Method:
    """
    A call that no signature accepts, by class, by length or by cast, may
    need a function of its own instead of an error.

    Parameters
    ----------

    func : Method
      A 'Callable[[Any, ...], Any]' receiving the call as it came, the
      instance first.

    Returns
    -------

    Method
      'func' itself.

    Raises
    ------

    TypeException
      'func' is not callable.

    DuplicateSignature
      A fallback is set already.
    """
    if not callable(func):
      raise TypeException('__fallback_func__', func, Func, MethodType)
    if self.__fallback_func__ is not None:
      raise DuplicateSignature('fallback', self.__fallback_func__, func)
    self.__fallback_func__ = self._adaptToKind(func)
    self.__compiled_func__ = None
    return func

  def setFinalizerFunction(self, func: Method) -> Method:
    """
    Some work must follow every dispatched call, whichever function was
    selected and whether or not it raised, as a 'finally' clause would.

    Implementation
    --------------

    The finalizer receives the arguments of the call. An exception it
    raises replaces that of the call, chained from it.

    Parameters
    ----------

    func : Method
      A 'Callable[[Any, ...], Any]' taking the instance first.

    Returns
    -------

    Method
      'func' itself.

    Raises
    ------

    TypeException
      'func' is not callable.

    DuplicateSignature
      A finalizer is set already.
    """
    if not callable(func):
      raise TypeException('__finalizer_func__', func, Func, MethodType)
    if self.__finalizer_func__ is not None:
      raise DuplicateSignature('finalizer', self.__finalizer_func__, func)
    self.__finalizer_func__ = self._adaptToKind(func)
    self.__compiled_func__ = None
    return func

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Callable:
    """
    An overloaded method must behave as a plain method does: read through
    the class it is a function taking the instance first, read through an
    instance it is bound to that instance. Nothing may be stored on the
    instance, since a stored bound method would be found by a dispatcher of
    the same name reached through 'super', copied along by 'copy.copy' and
    kept alive in a reference cycle.

    Implementation
    --------------

    Through the class the compiled function is returned, through an
    instance a new 'MethodType' of it on every read. A classmethod or a
    staticmethod gives a new 'MethodType' bound to the class, read through
    either. A dispatcher no class body placed, as one installed with
    'setattr', has no name to compile with.

    Parameters
    ----------

    instance : Any
      The instance read through, or 'None'.

    owner : type
      The class read through.

    Returns
    -------

    Callable
      The dispatch function, or a bound method of it.

    Raises
    ------

    MissingVariable
      No class body placed the dispatcher.
    """
    if owner is None:
      owner = type(instance)
    if self.__method_kind__ is not None:
      return MethodType(self._getCachedFunction(), owner)
    if instance is None:
      return self._getCachedFunction()
    return MethodType(self._getCachedFunction(), instance)

  def __set__(self, instance: Any, value: Any, **kwargs) -> Never:
    """
    An overloaded method must not be replaced through an instance.

    Raises
    ------

    ReadOnlyError
      Always.
    """
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any, **kwargs) -> Never:
    """
    An overloaded method must not be removed through an instance.

    Raises
    ------

    ProtectedError
      Always.
    """
    raise ProtectedError(instance, self, )

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A dispatcher must learn the class and name it is placed at, resolve
    'THIS' in its signatures to that class, and let a subclass react to
    the placement through 'hookSetName', as every 'Object' does.

    Implementation
    --------------

    'THIS' is replaced first, so the hook sees the signatures as the class
    will use them; then 'Object.__set_name__' records the owner and the
    name and calls 'hookSetName'.

    Parameters
    ----------

    owner : type
      The class the dispatcher is placed in.

    name : str
      The name it is placed at.
    """
    self.swapAllTHIS(owner)
    Object.__set_name__(self, owner, name, **kwargs)

  def __str__(self, ) -> str:
    owner = self.getFieldOwner()
    if owner is None:
      return '<%s object at %s>' % (type(self).__name__, hex(id(self)),)
    infoSpec = """Dispatcher at '%s.%s' for 'TypeSig' objects:<br><tab>%s"""
    ownerName = self.getFieldOwner().__name__
    fieldName = self.getFieldName()
    sigLines = [str(sig) for sig in self._getDeclaredSigs()]
    sigStr = '<br><tab>'.join(sigLines)
    info = infoSpec % (ownerName, fieldName, sigStr)
    return textFmt(info)

  __repr__ = __str__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _copySig(sig: TypeSig) -> TypeSig:
    """
    Placing a dispatcher rewrites 'THIS' in its signatures in place, so a
    clone sharing the signature objects of the original would fix 'THIS'
    for both.

    Implementation
    --------------

    A new signature of the same class gets the declared entries and the
    current ones.

    Parameters
    ----------

    sig : TypeSig
      The signature to copy.

    Returns
    -------

    TypeSig
      The copy.
    """
    copied = type(sig)(*sig.getDeclaredTypes())
    copied.__raw_types__ = sig.getRawTypes()
    return copied

  def clone(self, ) -> Self:
    """
    A namespace building on 'BaseSpace' may need a copy of a dispatcher
    for another class, holding the same registrations, without the copy
    and the original sharing anything that placement changes.

    Implementation
    --------------

    The copy holds the same functions with copies of the signatures and
    the same distances, fallback, finalizer and method kind, and no owner,
    name or compiled function. Its signatures hold the class of the
    original where 'THIS' was declared; 'restoreTHIS' on the copy, before
    it is placed, makes it resolve 'THIS' to its own class instead.

    Returns
    -------

    Dispatcher
      The copy.
    """
    newLoad = type(self)()
    sigFuncs = self._getSigFuncList()
    newLoad.__sig_funcs__ = [(self._copySig(s), f) for s, f in sigFuncs]
    newLoad.__sig_distances__ = [*self._getSigDistances(), ]
    variadicFuncs = self._getVariadicFuncs()
    if variadicFuncs:
      copies = [(self._copySig(s), f) for s, f in variadicFuncs]
      newLoad.__variadic_funcs__ = copies
      newLoad.__variadic_distances__ = [*self._getVariadicDistances(), ]
    flexFuncs = self._getFlexFuncs()
    if flexFuncs:
      copies = [(self._copySig(s), f) for s, f in flexFuncs]
      newLoad.__flex_funcs__ = copies
      newLoad.__flex_distances__ = [*self._getFlexDistances(), ]
    fallback = self._getFallbackFunction()
    if fallback is not None:
      newLoad.__fallback_func__ = fallback
    finalizer = self._getFinalizerFunction()
    if finalizer is not None:
      newLoad.__finalizer_func__ = finalizer
    newLoad.__method_kind__ = self.__method_kind__
    #  The wrappers of a staticmethod stay one per function on the copy.
    newLoad.__static_adapters__ = self.__static_adapters__
    return newLoad

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def restoreTHIS(self) -> None:
    """
    A clone of a placed dispatcher must resolve 'THIS' to the class it is
    placed on next.

    Implementation
    --------------

    Every signature is restored to its declared entries in place, and the
    compiled function is cleared. A dispatcher built by 'BaseSpace' shares
    its signature objects with the dispatchers of its bases and
    subclasses, so this is meant for clones, whose signatures are copies.
    """
    for sig, func in self._getSigFuncList():
      sig.restoreTHIS()
    for sig, func in self._getFlexFuncs():
      sig.restoreTHIS()
    for sig, func in self._getVariadicFuncs():
      sig.restoreTHIS()
    self.__compiled_func__ = None

  def swapAllTHIS(self, thisType: type) -> None:
    """
    Once the class holding the dispatcher exists, every signature declared
    with 'THIS' must match instances of it.

    Implementation
    --------------

    'THIS' is replaced by the class in every signature, in place, and the
    compiled function is cleared.

    Parameters
    ----------

    thisType : type
      The class holding the dispatcher.
    """
    for sig, func in self._getSigFuncList():
      sig.swapTHIS(thisType)
    for sig, func in self._getFlexFuncs():
      sig.swapTHIS(thisType)
    for sig, func in self._getVariadicFuncs():
      sig.swapTHIS(thisType)
    self.__compiled_func__ = None
