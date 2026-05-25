"""
Dispatcher encapsulates the mapping from type signature to function
objects and thus provides the core overloading functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from types import FunctionType as Func
from types import MethodType
from typing import TYPE_CHECKING

from ..core import Object
from ..utilities import maybe, typeCast, textFmt
from ..utilities.combinatorics import Arrangements
from ..waitaminute import TypeException, VariableNotNone, MissingVariable
from ..waitaminute.desc import ReadOnlyError, ProtectedError
from ..waitaminute.dispatch import DispatchException, DuplicateSignature
from . import TypeSig, PermuterMethod

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Never, TypeAlias, Optional, Self
  from . import Dispatcher

  Method: TypeAlias = Callable[[Any, ...], Any]
  Decorator: TypeAlias = Callable[[Method], Dispatcher]
  SigFuncList: TypeAlias = list[tuple[TypeSig, Method]]
  SigFuncMap: TypeAlias = dict[TypeSig, Method]


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
     signature of the call. This is the only pass that runs when the
     argument types are an exact match for a registered overload
     (e.g. 'f(69, 420)' against '@overload(int, int)'). Cost is one
     hash and one dict lookup. Use it by registering overloads whose
     'TypeSig' matches the exact concrete types the caller supplies.

  2. FAST - isinstance-checks each argument against a signature and
     returns the first match, in registration order: first the
     concrete signatures, then the variadic ones (a variadic matches
     when the call is longer than its fixed prefix). Cost is O(N) in
     the number of registered overloads. Runs only when FASTEST
     misses, i.e. the call relies on subclass-via-isinstance matching.

  3. SLOW - the same two passes (concrete, then variadic) as FAST but
     using 'typeCast' instead of 'isinstance', and only over
     signatures that allow coercion ('__allow_flex__'). Cost is O(N)
     plus a cast attempt per signature per argument. Runs only when
     FAST produced no match, i.e. the call relies on flexible type
     coercion ('@overload(int)' matching '"42"' via cast).

  The full order is FASTEST, FAST-concrete, FAST-variadic,
  SLOW-concrete, SLOW-variadic, then the fallback (if registered),
  else 'DispatchException'. With no variadic overloads registered the
  two variadic passes are empty and dispatch behaves as three tiers.

  Match selection in FAST and SLOW is first-registered-wins. The
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

  Performance contract
  --------------------
  FASTEST is roughly one or two orders of magnitude faster than FAST
  or SLOW on a non-trivial dispatcher. Imprecise overloads - those
  registered against abstract bases, broad union types, or types
  the caller is unlikely to supply directly - force every call to
  fall through FASTEST and into the FAST/SLOW iteration paths. For
  hot dispatch code this is a real cost, not a micro-optimization.

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
  __variadic_funcs__ = None
  __fallback_func__ = None
  __field_name__ = None
  __field_owner__ = None
  __finalizer_func__ = None
  __compiled_func__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getSigFuncList(self) -> SigFuncList:
    return maybe(self.__sig_funcs__, [])

  def _getSigFuncMap(self) -> SigFuncMap:
    return {sig: func for sig, func in self._getSigFuncList()}

  def _getVariadicFuncs(self) -> SigFuncList:
    """Return the list of '(variadicSig, func)' pairs registered for
    this dispatcher. Each variadicSig has a trailing 'ARGS'
    instance; the FAST and SLOW dispatch tiers iterate this list
    after the regular concrete sigs to match calls whose length
    exceeds what the FASTEST-tier expansion covers."""
    return maybe(self.__variadic_funcs__, [])

  def _getFallbackFunction(self) -> Optional[Method]:
    return self.__fallback_func__

  def _getFinalizerFunction(self) -> Optional[Method]:
    """
    Get the finalizer function if it exists.
    """
    return self.__finalizer_func__

  def _getFieldName(self, ) -> str:
    """Guarded variant of 'Object.getFieldName'. Raises
    'MissingVariable' if '__field_name__' has not been set yet
    (i.e. '__set_name__' has not fired)."""
    fieldName = self.__field_name__
    if fieldName is None:
      raise MissingVariable(self, '__field_name__', str)
    return fieldName

  def _getFieldOwner(self, ) -> type:
    """Guarded variant of 'Object.getFieldOwner'. Raises
    'MissingVariable' if '__field_owner__' has not been set yet
    (i.e. '__set_name__' has not fired)."""
    fieldOwner = self.__field_owner__
    if fieldOwner is None:
      raise MissingVariable(self, '__field_owner__', type)
    return fieldOwner

  def _getCachedKey(self, ) -> str:
    return '__bound_dispatch_%s__' % self._getFieldName()

  def _createCachedFunction(self) -> None:
    sigFuncMap = self._getSigFuncMap()
    variadicFuncs = self._getVariadicFuncs()
    fallback = self._getFallbackFunction()
    finalizer = self._getFinalizerFunction()
    dispatcher = self

    def dispatch(instance: Any, *args, **kwargs) -> Any:
      try:
        argSig = TypeSig.fromArgs(*args, )
        func = sigFuncMap.get(argSig, None)
        #  FASTEST
        if func is not None:
          return func(instance, *args, **kwargs)
        #  FAST
        for sig, func in sigFuncMap.items():
          if len(argSig) != len(sig):
            continue
          for arg, type_ in zip(args, sig):
            if not isinstance(arg, type_):
              break
          else:
            return func(instance, *args, **kwargs)
        #  FAST (variadic)
        for sig, func in variadicFuncs:
          rawTypes = sig._getRawTypes()
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
            return func(instance, *args, **kwargs)
        #  SLOW
        for sig, func in sigFuncMap.items():
          castArgs = []
          if not sig.__allow_flex__:
            continue
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
        for sig, func in variadicFuncs:
          if not sig.__allow_flex__:
            continue
          rawTypes = sig._getRawTypes()
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
        raise DispatchException(dispatcher, args, )
      finally:
        if callable(finalizer):
          _, exception, __ = sys.exc_info()
          try:
            finalizer(instance, *args, **kwargs)
          except Exception as finalException:
            if exception is None:
              raise finalException
            raise finalException from exception

    fieldName = self._getFieldName()
    ownerName = self._getFieldOwner().__name__
    dispatch.__name__ = fieldName
    dispatch.__qualname__ = '%s.%s' % (ownerName, fieldName)
    self.__compiled_func__ = dispatch

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

  def addSigFunc(self, sig: TypeSig, func: Method) -> Method:
    """
    Add a signature-function pair to the internal signature-function map.
    Raises 'DuplicateSignature' if a function is already registered
    under 'sig'.
    """
    existing = self._getSigFuncList()
    for existingSig, existingFunc in existing:
      if existingSig == sig:
        raise DuplicateSignature(sig, existingFunc, func)
    self.__sig_funcs__ = [*existing, (sig, func,)]
    self.__compiled_func__ = None
    return func

  def addVariadicSigFunc(self, sig: TypeSig, func: Method) -> Method:
    """Register a '(variadicSig, func)' pair on this dispatcher.

    Unlike 'addSigFunc', this does not reject duplicates: a repeated
    variadic signature is appended, and the first-registered one wins
    at dispatch. The caller must pass a 'sig' ending in an 'ARGS'
    sentinel; this is not validated here. The dispatcher matches
    calls against the variadic list in the FAST and SLOW passes when
    no concrete sig matches: the prefix raw types are
    isinstance-checked against the first '(len(sig) - 1)' call
    arguments, and every remaining argument is isinstance-checked
    against the 'ARGS' inner type."""
    existing = self._getVariadicFuncs()
    self.__variadic_funcs__ = [*existing, (sig, func,)]
    self.__compiled_func__ = None
    return func

  def setFallbackFunction(self, func: Method) -> Method:
    if not callable(func):
      raise TypeException('__fallback_func__', func, Func, MethodType)
    if self.__fallback_func__ is not None:
      raise VariableNotNone('__fallback_func__', self.__fallback_func__)
    self.__fallback_func__ = func
    self.__compiled_func__ = None
    return func

  def setFinalizerFunction(self, func: Method) -> Method:
    """
    Set the finalizer function that will be called when the dispatcher is
    deleted or finalized.
    """
    if not callable(func):
      raise TypeException('__finalizer_func__', func, Func, MethodType)
    if self.__finalizer_func__ is not None:
      raise VariableNotNone('__finalizer_func__', self.__finalizer_func__)
    self.__finalizer_func__ = func
    self.__compiled_func__ = None
    return func

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type, **kwargs) -> Callable:
    """
    Descriptor protocol method. Always returns a callable suitable
    for dispatching against the registered signatures:

    Class-level access ('Owner.attr') returns the compiled dispatch
    function with signature '(instance, *args, **kw)' - the same
    object Python would have produced for a plain method, so
    'Owner.attr(obj, ...)' dispatches against 'obj' as the first
    argument. The compiled function is built lazily by
    '_getCachedFunction' and cached on the 'Dispatcher' itself.

    Instance-level access ('obj.attr') returns a bound 'MethodType'
    wrapping that compiled function. The bound object is created on
    first access and cached on the instance under a reserved key
    derived from '_getCachedKey', so subsequent accesses on the
    same instance return the same bound object.

    The live 'Dispatcher' is no longer reachable through normal
    attribute access on the owning class. Reach it through
    'Owner.__dict__[name]' for introspection, post-hoc registration,
    or cloning.
    """
    if instance is None:
      return self._getCachedFunction()
    key = self._getCachedKey()
    try:
      boundCache = getattr(instance, key)
    except AttributeError as attributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      unboundCache = self._getCachedFunction()
      boundCache = MethodType(unboundCache, instance)
      setattr(instance, key, boundCache)
      return self.__get__(instance, owner, _recursion=True)
    else:
      return boundCache

  def __set__(self, instance: Any, value: Any, **kwargs) -> Never:
    """Illegal setter operation"""
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any, **kwargs) -> Never:
    """Illegal delete operation"""
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
    sigLines = []
    for sig, _ in self._getSigFuncList():
      sigLines.append(str(sig))
    sigStr = '<br><tab>'.join(sigLines)
    info = infoSpec % (ownerName, fieldName, sigStr)
    return textFmt(info)

  __repr__ = __str__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clone(self, ) -> Self:
    """Create a clone of this 'Dispatcher' carrying the same
    registered signature/function pairs (including variadic ones),
    the same fallback, and the same finalizer. The clone starts
    with an empty compiled-function cache and no field name or
    owner; those are populated when the clone is placed on a class
    and its '__set_name__' fires."""
    newLoad = type(self)()
    newLoad.__sig_funcs__ = self._getSigFuncList()
    variadicFuncs = self._getVariadicFuncs()
    if variadicFuncs:
      newLoad.__variadic_funcs__ = [*variadicFuncs, ]
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

  def overload(self, *types: type) -> Decorator:
    """Return a decorator that registers a function under the given
    positional-argument type signature. The decorator returns the
    dispatcher itself so subsequent '@dispatcher.overload(...)'
    layers stack on the same instance."""

    def decorator(func: Method) -> Self:
      self.addSigFunc(TypeSig(*types), func)
      return self

    return decorator

  def finalize(self, func: Method) -> Decorator:
    """Register 'func' as the finalizer. It runs in the 'finally'
    block of every dispatched call, after the body returns or raises.
    If the finalizer itself raises, its exception propagates in place
    of a normal return and is chained from any in-flight dispatch
    exception. Only one finalizer is allowed per dispatcher."""
    self.setFinalizerFunction(func)
    return self

  def fallback(self, func: Method) -> Decorator:
    """Register 'func' as the fallback. It runs after every pass has
    missed: not only on a type mismatch but also on a length
    mismatch, a coercion-disabled signature, or arguments only a
    keyword could satisfy (matching is positional and by length, and
    keyword arguments are not type-matched). Only one fallback is
    allowed per dispatcher."""
    self.setFallbackFunction(func)
    return self

  def flex(self, *types: type, ) -> Decorator:
    """Register 'func' under every ordering of the given types, so the
    caller may pass those arguments in any order. Each ordering is
    stored as a concrete signature with type coercion disabled (it is
    matched by isinstance in the FAST pass, never via 'typeCast'); a
    'PermuterMethod' restores the canonical argument order before
    calling 'func'. This is not a catch-all and not the fallback: only
    permutations of 'types' match. See 'fallback' for the no-match
    catch-all."""

    def decorator(func: Method) -> Self:
      for arrangement in Arrangements(*types):
        sig = TypeSig(*arrangement.values)
        sig.__allow_flex__ = False
        if TYPE_CHECKING:  # pragma: no cover
          assert isinstance(func, Func)
        load = PermuterMethod(func, arrangement)
        self.addSigFunc(sig, load)
      return self

    return decorator

  def swapAllTHIS(self, thisType: type) -> None:
    """
    Swap all occurrences of THIS in the registered signatures with the
    provided type. Walks both the concrete signature list and the
    variadic signature list. Invalidates the compiled-function
    cache, since 'TypeSig' hashes change with the swap.
    """
    for sig, func in self._getSigFuncList():
      sig.swapTHIS(thisType)
    for sig, func in self._getVariadicFuncs():
      sig.swapTHIS(thisType)
    self.__compiled_func__ = None
