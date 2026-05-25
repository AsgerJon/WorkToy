"""
The 'overload' function provides a decorator setting type signatures for
particular function overload. This overloading implementation requires
that the owning class is derived from 'BaseMeta' or a subclass of
'BaseMeta'. Other classes must use the 'Dispatcher' descriptor from
'worktoy.dispatch' instead.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..core.sentinels import ARGS
from ..utilities import maybe, textFmt
from ..utilities.combinatorics import Arrangements
from ..waitaminute import MissingVariable
from . import TypeSig, PermuterMethod

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias, Self, Iterator, Never

  Method: TypeAlias = Callable[..., Any]
  Decorator: TypeAlias = Callable[[Method], Any]
  Order: TypeAlias = tuple[int, ...]


class overload:  # NOQA
  """User-facing decorator that registers a type signature against a
  function so 'BaseMeta' can wire it into a 'Dispatcher' during
  class construction.

  Usage inside a class body:

  >>> from worktoy.mcls import BaseObject
  ...
  >>> class Frob(BaseObject):
  ...   @overload(int)
  ...   def __init__(self, n: int) -> None: pass
  ...   @overload(int, int)
  ...   def __init__(self, n: int, m: int) -> None: pass

  Stacking '@overload(...)' on a method registers each signature.
  The class's metaclass ('BaseMeta' or a subclass) sees the
  'overload' instance during namespace compilation and produces a
  'Dispatcher' descriptor that does the runtime dispatch.

  For classes whose metaclass is not 'BaseMeta'-based, use the
  'Dispatcher' descriptor directly.

  Class methods 'overload.flex', 'overload.fallback', and
  'overload.finalize' provide the same hooks as the corresponding
  'Dispatcher' methods.

  Performance and ordering
  ------------------------
  '@overload(SomeType)' produces a 'TypeSig' that the 'Dispatcher'
  matches in three tiers (see 'Dispatcher' docstring): exact-type
  hash lookup, then isinstance iteration, then 'typeCast'
  iteration. Only the first tier is constant-time; the other two
  scan every registered overload in registration order and return
  the first match.

  Two consequences for how you stack '@overload' decorators:

  1. Register against the exact concrete types callers will pass.
     '@overload(int)' for a caller that supplies 'int' values keeps
     the call on the constant-time tier. '@overload(SomeABC)' or
     '@overload(SomeUnionBase)' forces every matching call through
     O(N) iteration.

  2. When two overloads can both match the same call by
     isinstance, the one registered first wins. The dispatcher does
     not rank by specificity - it cannot, since a class with a
     custom '__instancecheck__' may legitimately want to absorb
     calls that would otherwise hit a "more specific" overload.
     Order your decorators to match the dispatch you want; treat
     overlapping isinstance coverage as deliberate, not as a bug
     for the dispatcher to second-guess.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __variadic_fastpath_limit__ = 5

  #  Private Variables
  __sig_func_dict__ = None
  __variadic_sig_func_list__ = None
  __next_sig__ = None
  __next_func__ = None
  __latest_func__ = None
  __fallback_func__ = None
  __finalizer_func__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getSigFuncDict(self) -> dict[TypeSig, Method]:
    return maybe(self.__sig_func_dict__, dict())

  def getVariadics(self) -> list[tuple[TypeSig, Method]]:
    """Return the list of (variadicSig, func) pairs registered on
    this overload. Each variadicSig has a trailing 'ARGS' instance
    as its last raw type; the dispatcher uses it to match calls
    whose length exceeds what the FASTEST-tier expansion covers."""
    return maybe(self.__variadic_sig_func_list__, [])

  def _getLatestFunc(self) -> Method:
    if self.__latest_func__ is None:
      raise RuntimeError(
        "no function has been registered on this 'overload' yet"
      )
    return self.__latest_func__

  def isFallback(self) -> bool:
    """Check if the current overload is a fallback function."""
    return False if self.__fallback_func__ is None else True

  def getFallback(self, ) -> Method:
    """Get the fallback function for the overload."""
    return self.__fallback_func__

  def isFinalizer(self) -> bool:
    """Check if the current overload is a finalizer function."""
    return False if self.__finalizer_func__ is None else True

  def getFinalizer(self, ) -> Method:
    """Get the finalizer function for the overload."""
    return self.__finalizer_func__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addSigFunc(self, sig: TypeSig, func: Method) -> None:
    """Register a (TypeSig, func) pair on this overload.

    If 'sig' ends in an 'ARGS' sentinel instance (variadic
    overload), the registration is expanded: the dispatcher's
    FASTEST tier gets concrete 'TypeSig' entries for every length
    from the prefix-only form up through prefix+N copies of the
    'ARGS' inner type, where N is 'cls.__variadic_fastpath_limit__'.
    A single variadic entry is also recorded in
    '__variadic_sig_func_list__' so the dispatcher can match calls
    whose length exceeds the FASTEST expansion."""
    raw = sig._getRawTypes()
    if raw and isinstance(raw[-1], ARGS):
      argsInst = raw[-1]
      innerType = argsInst.__inner_type__
      prefix = raw[:-1]
      existing = self._getSigFuncDict()
      limit = type(self).__variadic_fastpath_limit__
      for n in range(limit + 1):
        concreteTypes = (*prefix, *([innerType] * n))
        concrete = TypeSig(*concreteTypes)
        concrete.__allow_flex__ = sig.__allow_flex__
        existing[concrete] = func
      self.__sig_func_dict__ = existing
      variadics = self.getVariadics()
      self.__variadic_sig_func_list__ = [*variadics, (sig, func,)]
    else:
      existing = self._getSigFuncDict()
      existing[sig] = func
      self.__sig_func_dict__ = existing
    self.__latest_func__ = func

  def _extendLatest(self, sig: TypeSig) -> None:
    """Extend the latest function with a new signature."""
    self._addSigFunc(sig, self._getLatestFunc())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(cls, *types, **kwargs) -> Decorator:
    """Create a decorator that sets the type signature for the function."""

    if kwargs.get('_root', False):
      return super(overload, cls).__new__(cls)

    def decorator(func: Method) -> Self:
      sig = TypeSig(*types, )
      sig.__allow_flex__ = False if kwargs.get('strict', False) else True
      if isinstance(func, cls):
        func._extendLatest(sig)
        return func
      self = super(overload, cls).__new__(cls)
      self._addSigFunc(sig, func)
      return self

    return decorator

  def __init__(self, *args, **kwargs) -> None:
    pass

  @classmethod
  def flex(cls, *types: type) -> Decorator:
    """
    Creates a decorator that registers the function under every
    arrangement of the given canonical type signature.

    At dispatch time, the user supplies arguments in some arrangement of
    the canonical order. Each registered 'PermuterMethod' carries the
    'Arrangement' that produced its signature; the dispatcher uses
    'arrangement.restoreFrom(*args)' to permute the user's args back
    into canonical order before forwarding to 'func'.
    """

    def decorator(func: Method) -> Self:
      self = cls(_root=True)
      for arrangement in Arrangements(*types):
        sig = TypeSig(*arrangement.values)
        sig.__allow_flex__ = False
        if TYPE_CHECKING:  # pragma: no cover
          assert isinstance(func, FunctionType)
        load = PermuterMethod(func, arrangement)
        self._addSigFunc(sig, load)
      return self

    return decorator

  @classmethod
  def fallback(cls, func) -> Self:
    """Create a decorator that sets the fallback function for the
    overload."""
    self = cls(_root=True)
    self.__fallback_func__ = func
    return self

  @classmethod
  def finalize(cls, func: Method) -> Self:
    """Create a decorator that sets the finalizer function for the
    overload."""
    self = cls(_root=True)
    self.__finalizer_func__ = func
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getattr__(self, key: str) -> Any:
    funcs = [f for _, f in self._getSigFuncDict().items()]
    if funcs:
      func = funcs[0]
    elif self.isFallback():
      func = self.getFallback()
    else:
      raise MissingVariable(self, key)
    try:
      value = getattr(func, key)
    except AttributeError:
      raise MissingVariable(self, key)
    else:
      return value

  def __iter__(self, ) -> Iterator[tuple[TypeSig, Method]]:
    """Iterate over the signatures and functions in the overload."""
    yield from self._getSigFuncDict().items()

  if TYPE_CHECKING:  # pragma: no cover
    def __call__(self, func: Method) -> Never:
      """Linter friendly explicitly disabled call method. """

  def __str__(self, ) -> str:
    latestFunc = self._getLatestFunc()
    infoSpec = """overload of function: '%s', supporting type signatures: 
    <br><tab>%s"""
    sigLines = []
    for sig, _ in self._getSigFuncDict().items():
      sigLines.append(str(sig))
    sigStr = '<br><tab>'.join(sigLines)
    name = latestFunc.__name__
    info = infoSpec % (name, sigStr)
    return textFmt(info)

  __repr__ = __str__
