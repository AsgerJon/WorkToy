"""
Dispatcher maps type signatures to functions and resolves overloaded
calls to the matching one.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from types import MethodType
from typing import TYPE_CHECKING

from ..core import Object
from ..core.sentinels import ARGS
from ..utilities import maybe, typeCast, textFmt
from ..utilities.combinatorics import Arrangements
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import ReadOnlyError, ProtectedError
from ..waitaminute.dispatch import DispatchException, DuplicateSignature
from . import TypeSig, PermuterMethod, CallMeMaybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Never, TypeAlias, Optional, Self
  from . import Dispatcher

  Method: TypeAlias = Callable[[Any, ...], Any]
  Decorator: TypeAlias = Callable[[Method], Dispatcher]
  SigFuncList: TypeAlias = list[tuple[TypeSig, Method]]
  SigFuncMap: TypeAlias = dict[TypeSig, Method]


def _refuseMethodKinds(func: Any) -> None:
  """
  The '_refuseMethodKinds' function raises 'TypeException' for a
  staticmethod or a classmethod, and for anything that cannot be called,
  such as a 'property' stacked below a decorator or a bare value. A
  'Dispatcher' calls every function with the instance first, which
  neither kind takes: a staticmethod would receive the instance as its
  first argument, and a classmethod is not callable at all before Python
  3.10. An object that cannot be called used to be registered all the
  same and fail at the first call. 'overload' and the decorators of a
  'Dispatcher' wired by hand refuse through this one function.
  """
  if isinstance(func, (staticmethod, classmethod)) or not callable(func):
    raise TypeException('func', func, Func)


def _uniformType(types: tuple) -> Optional[type]:
  """
  The '_uniformType' function returns the one type every entry of 'types'
  is, or None when the entries differ. The trailing arguments of a call
  match a variadic signature by exact type only when they share one type,
  the inner type of its 'ARGS'.
  """
  first = types[0]
  for type_ in types:
    if type_ is not first:
      return None
  return first


class Dispatcher(Object):
  """
  Dispatcher encapsulates the mapping from type signature to function
  objects and thus provides the core overloading functionality.

  Dispatch tiers
  --------------
  Calls go through up to five ordered passes, returning at the first
  match. They group into three kinds (FASTEST, FAST, SLOW); FAST and
  SLOW each run first over concrete signatures, then over variadic
  ('ARGS'-terminated) signatures:

  1. FASTEST - a single 'dict.get' on the exact concrete-type
     signature of the call and, when that misses, one 'dict.get' per
     distinct prefix length among the variadic signatures, keyed by the
     prefix types and the one type every trailing argument shares. This
     is the only pass that runs when the argument types are an exact
     match for a registered overload (e.g. 'f(69, 420)' against
     '@overload(int, int)', or 'f(1, 2, 3, 4, 5, 6, 7)' against
     '@overload(ARGS[int])'), at any length. Cost is one hash and one
     dict lookup for each. Use it by registering overloads whose
     'TypeSig' matches the exact concrete types the caller supplies.
     Among exact matches the nearest registration wins: a variadic
     signature of a subclass takes a call an explicit signature of a
     parent also matches exactly, while a signature the subclass
     declares explicitly keeps its call. An exact match inherited from
     a farther class answers only when no registration of a nearer
     class accepts the call through 'isinstance'; see below.

  2. FAST - isinstance-checks each argument against a signature and
     returns the first match, class by class, nearest first; within a
     class first the concrete signatures in registration order, then
     the variadic ones, the most recent first (a variadic matches when
     the call is at least as long as its fixed prefix). Cost is O(N) in
     the number of registered overloads. Runs when FASTEST misses, i.e.
     the call relies on subclass-via-isinstance matching, and, over the
     nearer classes alone, before an exact match inherited from a
     farther class is taken.

  3. SLOW - the same two passes (concrete, then variadic) as FAST but
     using 'typeCast' instead of 'isinstance'. Cost is O(N) plus a cast
     attempt per signature per argument. Runs only when FAST produced
     no match, i.e. the call relies on a conversion 'typeCast' allows:
     within the number family and the text family, or through the
     '__cast_as__' of the target class ('@overload(float)' matching '1'
     via cast). No constructor is ever called on an argument, so a
     signature naming the class itself matches its instances alone
     unless the class declares '__cast_as__'.

  The full order is FASTEST, FAST (concrete, then variadic, class by
  class), SLOW-concrete, SLOW-variadic, then the fallback (if
  registered), else 'DispatchException'. With no variadic overloads
  registered the variadic passes are empty and dispatch behaves as
  three tiers.

  Keyword arguments
  -----------------
  A call dispatches on the types of its positional arguments alone, and
  its keyword arguments pass through unchanged to the function the
  positional types select, which refuses a keyword it does not take
  with its own 'TypeError'. The dispatcher names no parameter of its
  own a keyword could collide with, so 'instance=' and 'func=' pass
  through like any other keyword. A call with no positional arguments
  selects the empty signature, '@overload()', so a class that takes
  keywords declares that overload and handles them there, forwarding
  from its other overloads with 'if kwargs: self.__init__(**kwargs)'. A
  call no signature accepts goes to the fallback, else
  'DispatchException', which lists the keywords received.

  Within one class, match selection in FAST and SLOW is
  first-registered-wins. The
  dispatcher does not rank candidates by "specificity" - it cannot,
  in general. A metaclass with a custom '__instancecheck__' can make
  'isinstance(x, Number)' true for 'int' values intentionally, and
  the dispatcher has no way to tell whether the user meant 'Number'
  to be "broader than" 'int' or whether they explicitly want the
  Number overload to absorb int calls. If both overloads are
  registered, the one registered first wins. Order your overload
  decorators with this in mind: register the most specific
  signature you want to match first; any later, broader signature
  becomes a fallback for what the earlier ones did not catch.

  When 'BaseSpace' builds a 'Dispatcher' for a class, it registers the
  class body's own signatures first, followed by those inherited from
  the classes in its method resolution order, nearest first, each with
  its distance from the class. A registration of a nearer class wins
  every call it accepts, by exact type or through 'isinstance', ahead of
  any registration of a farther class: with '@overload(int)' inherited
  and '@overload(object)' declared in the subclass, 'f(1)' reaches the
  subclass, and so does a call of a further subclass that a 'THIS'
  signature of the subclass matches only through 'isinstance'. The
  inherited registrations keep the calls no nearer one accepts. SLOW
  tries the greatest distance first instead: a
  signature added in a subclass then only receives the calls none of
  the inherited signatures could take through a cast, and never
  redirects a call its parent already handled.

  Performance contract
  --------------------
  FASTEST is roughly one or two orders of magnitude faster than FAST
  or SLOW on a non-trivial dispatcher. Imprecise overloads - those
  registered against abstract bases, broad union types, or types
  the caller is unlikely to supply directly - force every call to
  fall through FASTEST and into the FAST/SLOW iteration paths. For
  hot dispatch code this is a real cost, not a micro-optimization. An
  exact match inherited from a farther class first costs an
  'isinstance' check of the registrations of the nearer classes, so a
  subclass overloading a name it inherits pays that on the calls its
  inherited signatures match.

  Practical rule: register signatures against the exact concrete
  types the caller will pass, not against ancestor classes. Use
  abstract or coerced overloads sparingly and only when the
  flexibility is intentionally part of the API.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __sig_funcs__ = None
  __sig_distances__ = None
  __variadic_funcs__ = None
  __variadic_distances__ = None
  __fallback_func__ = None
  __field_name__ = None
  __field_owner__ = None
  __finalizer_func__ = None
  __compiled_func__ = None
  #  The function the last of the decorators was given, which a decorator
  #  stacked above it registers; see '_stackedFunction'.
  __latest_func__ = None

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

  def _getDeclaredSigs(self) -> list[TypeSig]:
    """
    The '_getDeclaredSigs' method returns the signatures as they were
    declared: the concrete ones, then the variadic ones.
    """
    out = [sig for sig, _ in self._getSigFuncList()]
    out += [sig for sig, _ in self._getVariadicFuncs()]
    return out

  @staticmethod
  def _coversExactly(sig: TypeSig, types: tuple) -> bool:
    """
    The '_coversExactly' method reports whether the variadic signature
    'sig' accepts a call of exactly 'types' by exact type: the prefix by
    identity, and every type after it the inner type of the 'ARGS'.
    """
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

  def _getExactEntries(self) -> dict[TypeSig, tuple[int, Method]]:
    """
    The '_getExactEntries' method returns the mapping the exact-type pass
    reads, from each concrete signature to the distance and the function
    of the registration that takes a call of exactly those types. That is
    the concrete registration itself, unless a variadic signature from a
    nearer class accepts the same call by exact type; the nearer
    registration then wins, so a variadic override in a subclass takes
    every call it accepts, the ones a parent declared explicitly included.
    Of several nearer variadic signatures accepting the call, the most
    recent declaration of the nearest class wins, as in the tables of
    '_getExactVariadics'. A variadic signature of the same distance never
    displaces an explicit one. The distance tells the exact-type pass
    whether a nearer class must still be asked through 'isinstance'.
    """
    variadicFuncs = self._getVariadicFuncs()
    variadics = [*zip(variadicFuncs, self._getVariadicDistances())]
    out = dict()
    sigFuncs = self._getSigFuncList()
    for (sig, func), distance in zip(sigFuncs, self._getSigDistances()):
      types = sig.getRawTypes()
      best = None
      for index, ((variadic, nearerFunc), nearerDistance) in enumerate(
          variadics):
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
        out[sig] = (distance, func)
      else:
        out[sig] = (best[0][0], best[1])
    return out

  def _getExactVariadics(self) -> tuple[dict, dict, tuple[int, ...]]:
    """
    The '_getExactVariadics' method returns the tables the exact-type pass
    reads for the variadic signatures: one keyed by the prefix length,
    the prefix types and the inner type, for a call with trailing
    arguments, and one keyed by the prefix length and the prefix types
    alone, for a call of the prefix and nothing more, which every variadic
    signature of that prefix accepts whatever its inner type. Each entry
    holds a rank and the function, the rank being the distance of the
    class that declared it and then the declaration order reversed, so
    that of several signatures accepting one call the most recent one of
    the nearest class wins. The distinct prefix lengths come last,
    ascending.
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
    The '_getCastOrder' method returns the order in which the cast passes
    try the registrations: the greatest distance first, and registration
    order among equal distances. 'distances' lists the distance of each
    pair in 'sigFuncs', position by position. A signature inherited from
    a parent is therefore cast to before a signature its subclass added,
    so adding a signature in a subclass never redirects a call the parent
    already handled through a cast.

    Parameters
    ----------
    sigFuncs : SigFuncList
        Spells out to 'list[tuple[TypeSig, Method]]'. The registrations
        in registration order.
    distances : list[int]
        The distance of each registration, in the same order.

    Returns
    -------
    SigFuncList
        The same registrations in the order the cast passes try them.
    """
    #  Indexing rather than zipping raises 'IndexError' should the two
    #  lists ever fall out of step, where 'zip' would silently drop the
    #  unmatched registrations from the cast passes.
    positions = sorted(range(len(sigFuncs)), key=lambda i: -distances[i])
    return [sigFuncs[i] for i in positions]

  def _getVariadicOrder(self, nearestFirst: bool) -> SigFuncList:
    """
    The '_getVariadicOrder' method returns the variadic registrations in
    the order the 'isinstance' pass tries them, the nearest class first,
    or the cast passes, the farthest first, and within one class the
    most recent declaration first either way, so a later declaration
    takes a call an earlier one accepts as well.
    """
    pairs = self._getVariadicFuncs()
    distances = self._getVariadicDistances()
    sign = 1 if nearestFirst else -1
    positions = sorted(
        range(len(pairs)), key=lambda i: (sign * distances[i], -i),
    )
    return [pairs[i] for i in positions]

  def _getMatchTiers(self) -> list[tuple[int, SigFuncList, SigFuncList]]:
    """
    The '_getMatchTiers' method returns the registrations the 'isinstance'
    pass tries, grouped by distance, nearest class first, so a
    registration of a nearer class takes every call it accepts before any
    of a farther class is asked. Each group holds the concrete
    registrations of its distance in registration order, then the
    variadic ones with the most recent first.
    """
    concretes, variadics = dict(), dict()
    sigFuncs = self._getSigFuncList()
    for (sig, func), distance in zip(sigFuncs, self._getSigDistances()):
      concretes.setdefault(distance, []).append((sig, func))
    variadicFuncs = self._getVariadicFuncs()
    variadicDistances = self._getVariadicDistances()
    for index in reversed(range(len(variadicFuncs))):
      group = variadics.setdefault(variadicDistances[index], [])
      group.append(variadicFuncs[index])
    out = []
    for distance in sorted({*concretes, *variadics}):
      group = concretes.get(distance, []), variadics.get(distance, [])
      out.append((distance, *group))
    return out

  def _getFallbackFunction(self) -> Optional[Method]:
    return self.__fallback_func__

  def _getFinalizerFunction(self) -> Optional[Method]:
    return self.__finalizer_func__

  def _getFieldName(self, ) -> str:
    """
    The '_getFieldName' method is a guarded variant of
    'Object.getFieldName'.

    Returns
    -------
    str
        The field name assigned once this dispatcher is placed on a
        class.

    Raises
    ------
    MissingVariable
        If '__field_name__' has not been set yet, that is, if
        '__set_name__' has not fired.
    """
    fieldName = self.__field_name__
    if fieldName is None:
      raise MissingVariable(self, '__field_name__', str)
    return fieldName

  def _getFieldOwner(self, ) -> type:
    """
    The '_getFieldOwner' method is a guarded variant of
    'Object.getFieldOwner'.

    Returns
    -------
    type
        The class this dispatcher is placed on.

    Raises
    ------
    MissingVariable
        If '__field_owner__' has not been set yet, that is, if
        '__set_name__' has not fired.
    """
    fieldOwner = self.__field_owner__
    if fieldOwner is None:
      raise MissingVariable(self, '__field_owner__', type)
    return fieldOwner

  def _createCachedFunction(self) -> None:
    exactEntries = self._getExactEntries()
    tailed, empty, prefixLens = self._getExactVariadics()
    tiers = self._getMatchTiers()
    nearest = tiers[0][0] if tiers else 0
    castFuncs = self._getCastOrder(
        self._getSigFuncList(), self._getSigDistances(),
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

    def matchInstances(args: tuple, before: Optional[int], ) -> Any:
      """The function of the registration accepting 'args' through
      'isinstance', nearest class first, asking only the classes nearer
      than the distance 'before' when it is given; within a class the
      concrete signatures in registration order, then the variadic ones,
      the most recent first. None when none accepts the call."""
      for distance, concretes, variadics in tiers:
        if before is not None and distance >= before:
          return None
        for sig, func in concretes:
          if len(args) != len(sig):
            continue
          for arg, type_ in zip(args, sig):
            if not isinstance(arg, type_):
              break
          else:
            return func
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
            return func
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
        argSig = TypeSig.fromArgs(*args, )
        try:
          hit = exactEntries.get(argSig, None)
          if hit is None and prefixLens:
            hit = exactVariadic(argSig.getRawTypes())
        except TypeError:
          #  An argument whose class cannot be hashed misses the exact-type
          #  lookups and goes on to the 'isinstance' passes.
          hit = None
        #  FASTEST, unless a nearer class accepts the call through
        #  'isinstance': the match of the nearer class wins either way.
        if hit is not None:
          distance, func = hit
          if distance > nearest:
            nearer = matchInstances(args, distance)
            if nearer is not None:
              func = nearer
          return func(instance, *args, **kwargs)
        #  FAST, nearest class first
        func = matchInstances(args, None)
        if func is not None:
          return func(instance, *args, **kwargs)
        #  SLOW
        for sig, func in castFuncs:
          castArgs = []
          if len(argSig) != len(sig):
            continue
          for arg, type_ in zip(args, sig):
            if isinstance(arg, type_):
              castArgs.append(arg)
              continue
            try:
              castedArg = typeCast(type_, arg)
            except (ValueError, TypeError):
              break
            else:
              castArgs.append(castedArg)
          else:
            return func(instance, *castArgs, **kwargs)
        #  SLOW (variadic)
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
              castArgs.append(typeCast(type_, arg))
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
              castArgs.append(typeCast(innerType, arg))
            except (ValueError, TypeError):
              matched = False
              break
          if matched:
            return func(instance, *castArgs, **kwargs)
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
    dispatch.__doc__ = getattr(documented, '__doc__', None)
    self.__compiled_func__ = dispatch

  def _getDocumentedFunction(self) -> Optional[Method]:
    """
    The '_getDocumentedFunction' method returns the function whose
    docstring the compiled dispatch carries: the first concrete
    registration, else the first variadic one, else the fallback, else
    None. A registration the dispatcher wraps itself, the 'PermuterMethod'
    of a flexible declaration, is documented by the function it wraps:
    read as an attribute, the wrapper answers with the docstring of its
    own class, since the lookup finds that before 'CallMeMaybe.__getattr__'
    could hand over to the function. The owner's module is the dispatch's
    module, so 'help' and the documentation tools see the method where the
    author wrote it.
    """
    for _, func in self._getSigFuncList():
      return self._unwrapCallMeMaybe(func)
    for _, func in self._getVariadicFuncs():
      return self._unwrapCallMeMaybe(func)
    return self._unwrapCallMeMaybe(self._getFallbackFunction())

  @staticmethod
  def _unwrapCallMeMaybe(func: Any) -> Any:
    """
    The '_unwrapCallMeMaybe' method returns the function a 'CallMeMaybe'
    wraps, and anything else as it is.
    """
    if isinstance(func, CallMeMaybe):
      return func.__wrapped__
    return func

  def _getCachedFunction(self, **kwargs) -> Callable:
    if self.__compiled_func__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createCachedFunction()
      return self._getCachedFunction(_recursion=True)
    return self.__compiled_func__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addSigFunc(
      self,
      sig: TypeSig,
      func: Method,
      distance: int = 0,
  ) -> Method:
    """
    The 'addSigFunc' method adds a signature-function pair to the
    internal signature-function map.

    Parameters
    ----------
    sig : TypeSig
        The type signature to register the function under.
    func : Method
        The function to register. 'Method' expands to
        'Callable[[Any, ...], Any]'.
    distance : int, optional
        How far from the owning class the registration comes: 0 for the
        owning class itself, 1 for the nearest class it inherits the
        registration from, and so on. The exact-type and isinstance
        passes prefer the smallest distance: a registration of a nearer
        class takes every call it accepts ahead of one of a farther
        class. The cast passes try the greatest distance first.
        Defaults to 0.

    Returns
    -------
    Method
        The same 'func', so the method can sit at the end of a
        registration chain.

    Raises
    ------
    DuplicateSignature
        If a function is already registered under 'sig'.
    """
    self._resolveTHIS(sig)
    existing = self._getSigFuncList()
    for existingSig, existingFunc in existing:
      if existingSig == sig:
        raise DuplicateSignature(sig, existingFunc, func)
    self.__sig_funcs__ = [*existing, (sig, func,)]
    self.__sig_distances__ = [*self._getSigDistances(), distance]
    self.__compiled_func__ = None
    return func

  def addVariadicSigFunc(
      self,
      sig: TypeSig,
      func: Method,
      distance: int = 0,
  ) -> Method:
    """
    The 'addVariadicSigFunc' method registers a '(variadicSig, func)'
    pair on this dispatcher. Unlike 'addSigFunc', it does not reject
    duplicates: a repeated variadic signature is appended, and of several
    accepting one call the most recent of the nearest class wins at
    dispatch. The dispatcher matches a call
    against the variadic signatures by exact type in the FASTEST pass,
    the prefix types and the one type the trailing arguments share as
    the key, and in the FAST and SLOW passes when no concrete signature
    matches, isinstance-checking the prefix raw types against the first
    '(len(sig) - 1)' call arguments and every remaining argument against
    the 'ARGS' inner type.

    Parameters
    ----------
    sig : TypeSig
        The variadic signature, which must end in an 'ARGS' sentinel.
        This is not validated here.
    func : Method
        The function to register. 'Method' expands to
        'Callable[[Any, ...], Any]'.
    distance : int, optional
        How far from the owning class the registration comes, with the
        same meaning as in 'addSigFunc'. Defaults to 0.

    Returns
    -------
    Method
        The same 'func', so the method can sit at the end of a
        registration chain.
    """
    self._resolveTHIS(sig)
    existing = self._getVariadicFuncs()
    self.__variadic_funcs__ = [*existing, (sig, func,)]
    self.__variadic_distances__ = [*self._getVariadicDistances(), distance]
    self.__compiled_func__ = None
    return func

  def _resolveTHIS(self, sig: TypeSig) -> None:
    """
    The '_resolveTHIS' method rewrites 'THIS' in 'sig' to the owning
    class when this dispatcher is already placed on one, so a signature
    registered after '__set_name__' resolves as one registered before.
    A dispatcher not yet placed leaves the sentinel for '__set_name__'.
    """
    owner = self.__field_owner__
    if owner is not None:
      sig.swapTHIS(owner)

  def setFallbackFunction(self, func: Method) -> Method:
    """
    The 'setFallbackFunction' method registers the fallback, run when no
    registered signature matches a dispatched call.

    Parameters
    ----------
    func : Method
        The fallback to register. 'Method' expands to
        'Callable[[Any, ...], Any]'.

    Returns
    -------
    Method
        The same 'func', so the method can sit at the end of a
        registration chain.

    Raises
    ------
    TypeException
        If 'func' is not callable.
    DuplicateSignature
        If a fallback is already set, with 'fallback' in place of the
        signature, as for a second registration of one signature.
    """
    if not callable(func):
      raise TypeException('__fallback_func__', func, Func, MethodType)
    if self.__fallback_func__ is not None:
      raise DuplicateSignature('fallback', self.__fallback_func__, func)
    self.__fallback_func__ = func
    self.__compiled_func__ = None
    return func

  def setFinalizerFunction(self, func: Method) -> Method:
    """
    The 'setFinalizerFunction' method registers the finalizer. Like a
    'finally' clause, the finalizer runs at the end of every dispatched
    call no matter which overload was selected, and it runs even when the
    body raised, including a 'DispatchException' from no overload
    matching. If the finalizer itself raises while an exception is
    already in flight, its exception is chained from the in-flight one.

    Parameters
    ----------
    func : Method
        The finalizer to register. 'Method' expands to
        'Callable[[Any, ...], Any]'.

    Returns
    -------
    Method
        The same 'func', so the method can sit at the end of a
        registration chain.

    Raises
    ------
    TypeException
        If 'func' is not callable.
    DuplicateSignature
        If a finalizer is already set, with 'finalizer' in place of the
        signature.
    """
    if not callable(func):
      raise TypeException('__finalizer_func__', func, Func, MethodType)
    if self.__finalizer_func__ is not None:
      raise DuplicateSignature('finalizer', self.__finalizer_func__, func)
    self.__finalizer_func__ = func
    self.__compiled_func__ = None
    return func

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Callable:
    """
    The '__get__' method is the descriptor protocol entry point. It
    always returns a callable suitable for dispatching against the
    registered signatures.

    Class-level access ('Owner.attr') returns the compiled dispatch
    function, which takes the instance as its first positional argument,
    as the function of a plain method takes 'self', so
    'Owner.attr(obj, ...)' dispatches against 'obj' as the first
    argument. It takes the instance by position without naming it, so no
    keyword of a call collides with a parameter of its own. The compiled
    function is built lazily by '_getCachedFunction' and cached on the
    'Dispatcher' itself.

    Instance-level access ('obj.attr') returns a fresh bound
    'MethodType' wrapping that compiled function on every access, just
    as Python does for a plain method. Nothing is stored on the
    instance. A bound method stored there would be found again by
    whichever 'Dispatcher' of the same name reads the instance next,
    such as the parent's 'Dispatcher' reached through 'super'. It would
    also be carried along by 'copy.copy', still bound to the original,
    and it would keep the instance alive through a reference cycle.

    The live 'Dispatcher' is no longer reachable through normal
    attribute access on the owning class. Reach it through
    'Owner.__dict__[name]' for introspection, post-hoc registration,
    or cloning.

    A dispatcher installed on a finished class with 'setattr' never
    receives '__set_name__'. The first read through that class adopts
    the class holding it and the name it is held under; see
    '_adoptOwner'.

    Parameters
    ----------
    instance : Any
        The instance the attribute is read from, or None on
        class-level access.
    owner : type
        The class the descriptor is attached to.

    Returns
    -------
    Callable
        On class-level access, the compiled dispatch function; on
        instance-level access, a bound 'MethodType' wrapping it.
    """
    self._adoptOwner(owner if owner is not None else type(instance))
    if instance is None:
      return self._getCachedFunction()
    return MethodType(self._getCachedFunction(), instance)

  def _adoptOwner(self, owner: type) -> None:
    """
    The '_adoptOwner' method names this dispatcher, when nothing has yet,
    after the class along the resolution order of 'owner' that holds it
    and the name it is held under, by running '__set_name__' as the class
    statement would have. A dispatcher installed with 'setattr' is the
    one this serves; a placed dispatcher is left as it is, and one no
    class holds is left unnamed, to be refused as before. The resolution
    order is read with 'type.__getattribute__', so that no reimplemented
    '__getattribute__' of the owner can answer for it.
    """
    if self.__field_owner__ is not None:
      return
    try:
      mro = type.__getattribute__(owner, '__mro__')
    except (AttributeError, TypeError):
      mro = (owner,)
    for cls in mro:
      for name, value in cls.__dict__.items():
        if value is self:
          self.__set_name__(cls, name)
          return

  def __set__(self, instance: Any, value: Any, **kwargs) -> Never:
    """
    A 'Dispatcher' is read-only, so the '__set__' method always raises.

    Raises
    ------
    ReadOnlyError
        On every call.
    """
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any, **kwargs) -> Never:
    """
    A 'Dispatcher' is protected, so the '__delete__' method always
    raises.

    Raises
    ------
    ProtectedError
        On every call.
    """
    raise ProtectedError(instance, self, )

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner
    self.swapAllTHIS(owner)

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
    The '_copySig' method returns a copy of 'sig' holding the same types
    and the same declared types.
    '__set_name__' rewrites 'THIS' in the signatures of a dispatcher in
    place, so a clone holding the signatures of the original would fix
    'THIS' for both. The copy keeps the declared types so that
    'restoreTHIS' can put the sentinel back on the clone.
    """
    copied = type(sig)(*sig.getDeclaredTypes())
    copied.__raw_types__ = sig.getRawTypes()
    return copied

  def clone(self, ) -> Self:
    """
    The 'clone' method builds a copy of this 'Dispatcher' carrying the
    same registered signature/function pairs (including variadic ones)
    with their distances, the same fallback, and the same finalizer.

    The signatures are copies, see '_copySig', so placing the clone on a
    class resolves 'THIS' in its own signatures alone. A clone of a
    placed dispatcher carries the class of the original in place of
    'THIS', as the original does, so a subclass may add a 'THIS' overload
    of its own beside the inherited one; 'restoreTHIS' on the clone puts
    the sentinel back before placement, so the clone resolves 'THIS' to
    the class it is placed on instead.

    Returns
    -------
    Self
        A new 'Dispatcher' with an empty compiled-function cache and no
        field name or owner. Those are populated when the clone is
        placed on a class and its '__set_name__' fires.
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
    fallback = self._getFallbackFunction()
    if fallback is not None:
      newLoad.__fallback_func__ = fallback
    finalizer = self._getFinalizerFunction()
    if finalizer is not None:
      newLoad.__finalizer_func__ = finalizer
    return newLoad

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _stackedFunction(self, func: Any) -> Method:
    """
    The '_stackedFunction' method returns the function a decorator of this
    dispatcher registers. Each decorator returns the dispatcher, so one
    stacked above another receives the dispatcher itself, and registers
    the function the decorator below it was given instead: a stack
    decorates one function, and each decorator in it adds one role for
    that function, in any order. Given a function, it records it for the
    decorators above.

    Raises
    ------
    MissingVariable
        If the dispatcher is given itself before any function.
    TypeException
        If the function is a staticmethod, a classmethod or cannot be
        called; see '_refuseMethodKinds'.
    """
    if func is self:
      if self.__latest_func__ is None:
        raise MissingVariable(self, '__latest_func__', Func)
      return self.__latest_func__
    _refuseMethodKinds(func)
    self.__latest_func__ = func
    return func

  def overload(self, *types: type) -> Decorator:
    """
    The 'overload' method builds a decorator that registers the
    decorated function under the given positional-argument type
    signature. The decorator returns the dispatcher itself, so
    successive '@dispatcher.overload(...)' layers stack on the same
    instance, each registering the one function of the stack; see
    '_stackedFunction'. A signature ending in an 'ARGS' is registered as a
    variadic one, through 'addVariadicSigFunc', so it takes calls of any
    length from its fixed prefix on.

    Parameters
    ----------
    *types : type
        The positional-argument types of the signature.

    Returns
    -------
    Decorator
        A decorator registering its function and returning this
        dispatcher. 'Decorator' expands to
        'Callable[[Method], Dispatcher]'.

    Raises
    ------
    TypeException
        If an entry is not a class, or an 'ARGS' of one at the end; see
        'TypeSig.validateTypes'.
    """
    types = TypeSig.starARGS(*types)
    TypeSig.validateTypes(*types)

    def decorator(func: Method) -> Self:
      func = self._stackedFunction(func)
      sig = TypeSig(*types)
      if types and isinstance(types[-1], ARGS):
        self.addVariadicSigFunc(sig, func)
      else:
        self.addSigFunc(sig, func)
      return self

    return decorator

  def finalize(self, func: Method) -> Self:
    """
    The 'finalize' method registers 'func' as the finalizer. It runs in
    the 'finally' block of every dispatched call, after the body returns
    or raises. If the finalizer itself raises, its exception propagates
    in place of a normal return and is chained from any in-flight
    dispatch exception. Only one finalizer is allowed per dispatcher.
    Stacked on another decorator of this dispatcher, it registers the
    function of the stack; see '_stackedFunction'.

    Parameters
    ----------
    func : Method
        The finalizer to register. 'Method' expands to
        'Callable[[Any, ...], Any]'.

    Returns
    -------
    Self
        This dispatcher, so used as a decorator it binds the decorated
        name to the same instance.
    """
    self.setFinalizerFunction(self._stackedFunction(func))
    return self

  def fallback(self, func: Method) -> Self:
    """
    The 'fallback' method registers 'func' as the fallback. It runs
    after every pass has missed: not only on a type mismatch but also on
    a length mismatch, a coercion-disabled signature, or a keyword call
    binding no registration. Only one fallback is allowed
    per dispatcher. Stacked on another decorator of this dispatcher, it
    registers the function of the stack; see '_stackedFunction'.

    Parameters
    ----------
    func : Method
        The fallback to register. 'Method' expands to
        'Callable[[Any, ...], Any]'.

    Returns
    -------
    Self
        This dispatcher, so used as a decorator it binds the decorated
        name to the same instance.
    """
    self.setFallbackFunction(self._stackedFunction(func))
    return self

  def flex(self, *types: type, ) -> Decorator:
    """
    The 'flex' method builds a decorator that registers its function
    under every ordering of the given types, so the caller may pass
    those arguments in any order. Each ordering is stored as a concrete
    signature, and a 'PermuterMethod' restores the canonical argument
    order before calling the function.
    This is not a catch-all and not the fallback: only permutations of
    'types' match. See 'fallback' for the no-match catch-all. Stacked on
    another decorator of this dispatcher, it registers the function of
    the stack; see '_stackedFunction'.

    Parameters
    ----------
    *types : type
        The canonical positional-argument types. Every ordering of
        them is registered.

    Returns
    -------
    Decorator
        A decorator registering its function and returning this
        dispatcher. 'Decorator' expands to
        'Callable[[Method], Dispatcher]'.

    Raises
    ------
    TypeException
        If an entry is not a class; an 'ARGS' is refused too, since the
        entries are rearranged.
    """
    types = TypeSig.starARGS(*types)
    TypeSig.validateTypes(*types, variadic=False)

    def decorator(func: Method) -> Self:
      func = self._stackedFunction(func)
      for arrangement in Arrangements(*types):
        sig = TypeSig(*arrangement.values)
        if TYPE_CHECKING:  # pragma: no cover
          assert isinstance(func, Func)
        load = PermuterMethod(func, arrangement)
        self.addSigFunc(sig, load)
      return self

    return decorator

  def restoreTHIS(self) -> None:
    """
    The 'restoreTHIS' method puts 'THIS' back in every registered
    signature that was declared with it, concrete and variadic, undoing
    'swapAllTHIS', and invalidates the compiled-function cache. On a
    clone made from a placed dispatcher this lets the clone resolve
    'THIS' to the class it is placed on next.
    """
    for sig, func in self._getSigFuncList():
      sig.restoreTHIS()
    for sig, func in self._getVariadicFuncs():
      sig.restoreTHIS()
    self.__compiled_func__ = None

  def swapAllTHIS(self, thisType: type) -> None:
    """
    The 'swapAllTHIS' method replaces every occurrence of THIS in the
    registered signatures with the provided type, walking both the
    concrete signature list and the variadic signature list. It
    invalidates the compiled-function cache, since 'TypeSig' hashes
    change with the swap.

    Parameters
    ----------
    thisType : type
        The class to substitute for the THIS sentinel, supplied once
        the enclosing class exists.
    """
    for sig, func in self._getSigFuncList():
      sig.swapTHIS(thisType)
    for sig, func in self._getVariadicFuncs():
      sig.swapTHIS(thisType)
    self.__compiled_func__ = None
