"""
The 'overload' decorator registers a type signature for one overloaded
function.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..core.sentinels import ARGS
from ..utilities import maybe, textFmt, NoPickle
from ..utilities.combinatorics import Arrangements
from ..waitaminute import MissingVariable, TypeException
from . import TypeSig, PermuterMethod

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias, Self, Iterator, Never

  Method: TypeAlias = Callable[..., Any]
  Decorator: TypeAlias = Callable[[Method], Any]
  Order: TypeAlias = tuple[int, ...]


class overload(NoPickle):  # NOQA
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

  Decorators stacked on one function each add a role for that function,
  in any order. '@overload(str)' above '@overload.fallback' makes the
  function both the 'str' overload and the fallback, and '@overload(str)'
  above '@overload.flex(str, int)' registers the function for a lone
  'str' beside both orders of 'str' and 'int':

  >>> class Label(BaseObject):
  ...   @overload(str)
  ...   @overload.flex(str, int)
  ...   def __init__(self, text: str, size: int = 12) -> None: pass

  Performance and ordering
  ------------------------
  '@overload(SomeType)' produces a 'TypeSig' that the 'Dispatcher'
  matches in three kinds of pass (see 'Dispatcher' docstring):
  exact-type hash lookup, then isinstance iteration, then 'typeCast'
  iteration. Only the first is constant-time; the other two scan
  every registered overload in order and return the first match.
  Within one class body that order is the declaration order.

  Three consequences for how you stack '@overload' decorators:

  1. Register against the exact concrete types callers will pass.
     '@overload(int)' for a caller that supplies 'int' values keeps
     the call on the constant-time pass. '@overload(SomeABC)' or
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

  3. A subclass overloading an inherited name keeps the inherited
     overloads and adds its own. Its own come first in the exact-type
     and isinstance passes, so an override wins wherever it matches,
     and an equal signature replaces the inherited one outright. The
     'typeCast' pass tries the inherited overloads first, so a
     signature the subclass adds never takes a call its parent
     already handled through a cast.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    """
    The 'getVariadics' method returns the list of '(variadicSig, func)'
    pairs registered on this overload. Each variadicSig has a trailing
    'ARGS' instance as its last raw type, and the dispatcher matches a
    call of any length against it, the prefix by type and every trailing
    argument against the inner type of the 'ARGS'.

    Returns
    -------
    list of tuple of (TypeSig, Method)
        The registered variadic pairs. 'Method' expands to
        'Callable[..., Any]'.
    """
    return maybe(self.__variadic_sig_func_list__, [])

  def _getLatestFunc(self) -> Method:
    if self.__latest_func__ is None:
      raise RuntimeError(
        "no function has been registered on this 'overload' yet"
      )
    return self.__latest_func__

  def isFallback(self) -> bool:
    """True when a fallback function has been registered on this
    overload."""
    return False if self.__fallback_func__ is None else True

  def getFallback(self, ) -> Method:
    """The fallback function registered on this overload, or None."""
    return self.__fallback_func__

  def isFinalizer(self) -> bool:
    """True when a finalizer function has been registered on this
    overload."""
    return False if self.__finalizer_func__ is None else True

  def getFinalizer(self, ) -> Method:
    """The finalizer function registered on this overload, or None."""
    return self.__finalizer_func__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addSigFunc(self, sig: TypeSig, func: Method) -> None:
    """
    The '_addSigFunc' method registers a '(TypeSig, func)' pair on this
    overload. A signature ending in an 'ARGS' sentinel instance, a
    variadic declaration, is recorded once in
    '__variadic_sig_func_list__', as written, and the dispatcher matches
    calls of any length against it. Every other signature is recorded in
    the concrete mapping, where an equal signature stacked again keeps
    the place it first took.

    Parameters
    ----------
    sig : TypeSig
        The signature to register, possibly ending in an 'ARGS'
        sentinel.
    func : Method
        The function to register. 'Method' expands to
        'Callable[..., Any]'.
    """
    raw = sig.getRawTypes()
    if raw and isinstance(raw[-1], ARGS):
      variadics = self.getVariadics()
      self.__variadic_sig_func_list__ = [*variadics, (sig, func,)]
    else:
      existing = self._getSigFuncDict()
      existing[sig] = func
      self.__sig_func_dict__ = existing
    self.__latest_func__ = func

  def _extendLatest(self, sig: TypeSig) -> None:
    """
    The '_extendLatest' method registers another signature against the
    most recently added function, so stacked '@overload(...)' decorators
    all resolve to the same function body.

    Parameters
    ----------
    sig : TypeSig
        The additional signature to register against the latest
        function.
    """
    self._addSigFunc(sig, self._getLatestFunc())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(cls, *types, **kwargs) -> Decorator:
    """
    The 'overload' constructor returns a decorator that registers the
    decorated function under the given positional-argument type
    signature.

    Parameters
    ----------
    *types : type
        The positional-argument types of the signature.
    **kwargs
        strict : bool, optional
            Whether the signature refuses casts: a strict signature
            matches a call by exact type or 'isinstance' alone, and the
            cast passes of the 'Dispatcher' skip it. Defaults to False.

    Returns
    -------
    Decorator
        A decorator registering its function and returning the 'overload'
        instance. 'Decorator' expands to 'Callable[[Method], Any]'.

    Raises
    ------
    TypeException
        If an entry is not a class, or an 'ARGS' of one at the end; see
        'TypeSig.validateTypes'.
    TypeError
        If a keyword is any other than 'strict'.
    """

    if kwargs.get('_root', False):
      return super(overload, cls).__new__(cls)
    cls._refuseKeywords(**kwargs)
    TypeSig.validateTypes(*types)

    def decorator(func: Method) -> Self:
      sig = TypeSig(*types, )
      sig.__allow_flex__ = False if kwargs.get('strict', False) else True
      if isinstance(func, cls):
        func._extendLatest(sig)
        return func
      cls._refuseMethodKinds(func)
      self = super(overload, cls).__new__(cls)
      self._addSigFunc(sig, func)
      return self

    return decorator

  def __init__(self, *args, **kwargs) -> None:
    pass

  @classmethod
  def flex(cls, *types: type) -> Decorator:
    """
    The 'flex' decorator factory returns a decorator that registers the
    function under every arrangement of the given canonical type
    signature.

    At dispatch time, the user supplies arguments in some arrangement of
    the canonical order. Each registered 'PermuterMethod' carries the
    'Arrangement' that produced its signature. When the dispatcher
    selects it, that 'PermuterMethod' (not the dispatcher) calls
    'arrangement.restoreFrom(*args)' to permute the caller's arguments
    back into canonical order, then invokes 'func'.

    Parameters
    ----------
    *types : type
        The canonical positional-argument types. Every ordering of them
        is registered.

    Returns
    -------
    Decorator
        A decorator registering its function and returning the 'overload'
        instance. 'Decorator' expands to 'Callable[[Method], Any]'.

    Raises
    ------
    TypeException
        If an entry is not a class; an 'ARGS' is refused too, since the
        entries are rearranged.
    """
    TypeSig.validateTypes(*types, variadic=False)

    def decorator(func: Method) -> Self:
      self, function = cls._stackOn(func)
      for arrangement in Arrangements(*types):
        sig = TypeSig(*arrangement.values)
        sig.__allow_flex__ = False
        if TYPE_CHECKING:  # pragma: no cover
          assert isinstance(function, FunctionType)
        load = PermuterMethod(function, arrangement)
        self._addSigFunc(sig, load)
      #  A decorator stacked above registers the function itself, not the
      #  wrapper of the last arrangement.
      self.__latest_func__ = function
      return self

    return decorator

  @classmethod
  def fallback(cls, func) -> Self:
    """
    The 'fallback' classmethod registers 'func' as the fallback, invoked
    when no signature matches a dispatched call.

    Parameters
    ----------
    func : Method
        The fallback function. 'Method' expands to 'Callable[..., Any]'.

    Returns
    -------
    Self
        The 'overload' carrying the fallback: the one from a decorator
        below in the same stack, or a new one.
    """
    self, function = cls._stackOn(func)
    self.__fallback_func__ = function
    return self

  @classmethod
  def finalize(cls, func: Method) -> Self:
    """
    The 'finalize' classmethod registers 'func' as the finalizer, run in
    the 'finally' block of every dispatched call.

    Parameters
    ----------
    func : Method
        The finalizer function. 'Method' expands to 'Callable[..., Any]'.

    Returns
    -------
    Self
        The 'overload' carrying the finalizer: the one from a decorator
        below in the same stack, or a new one.
    """
    self, function = cls._stackOn(func)
    self.__finalizer_func__ = function
    return self

  @classmethod
  def _stackOn(cls, func: Any) -> tuple[Self, Method]:
    """
    The '_stackOn' method returns the 'overload' a role decorator, 'flex',
    'fallback' or 'finalize', adds its role to, with the function the role
    is for. Given an 'overload' from a decorator below in the same stack,
    it returns that one, with the function the stack decorates, so every
    decorator of the stack registers one function. Given the function
    itself, it returns a new 'overload' decorating it, after refusing a
    staticmethod or a classmethod.
    """
    if isinstance(func, cls):
      return func, func._getLatestFunc()
    cls._refuseMethodKinds(func)
    self = cls(_root=True)
    self.__latest_func__ = func
    return self, func

  @staticmethod
  def _refuseKeywords(**kwargs) -> None:
    """
    The '_refuseKeywords' method raises the 'TypeError' Python raises for
    an unexpected keyword argument, for any keyword the decorator does not
    take. A misspelled 'strict' would otherwise leave the signature open
    to casts without a word.
    """
    for key in kwargs:
      if key != 'strict':
        infoSpec = """overload() got an unexpected keyword argument '%s'"""
        raise TypeError(infoSpec % key)

  @staticmethod
  def _refuseMethodKinds(func: Any) -> None:
    """
    The '_refuseMethodKinds' method raises 'TypeException' for a
    staticmethod or a classmethod. The 'Dispatcher' an overload builds
    calls every function with the instance first, which neither kind
    takes: a staticmethod would receive the instance as its first
    argument, and a classmethod is not callable at all before Python 3.10.
    """
    if isinstance(func, (staticmethod, classmethod)):
      raise TypeException('func', func, FunctionType)

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
    """
    Iterating an 'overload' yields each concrete '(TypeSig, function)'
    pair registered on it; the variadic pairs are read from
    'getVariadics'.

    Yields
    ------
    tuple of (TypeSig, Method)
        Each registered signature-function pair. 'Method' expands to
        'Callable[..., Any]'.
    """
    yield from self._getSigFuncDict().items()

  if TYPE_CHECKING:  # pragma: no cover
    def __call__(self, func: Method) -> Never:
      """Linter friendly explicitly disabled call method. """

  def __str__(self, ) -> str:
    """
    The string representation names the function the overload decorates
    and lists each role it registers the function in: every type
    signature, the variadic ones after the concrete, then the fallback
    and the finalizer, as a stack of decorators may combine them. An
    instance with no function yet renders a short note instead of
    raising.
    """
    if self.__latest_func__ is None:
      return textFmt("""overload with no function registered so far""")
    roles = [str(sig) for sig, _ in self._getSigFuncDict().items()]
    roles += [str(sig) for sig, _ in self.getVariadics()]
    if self.isFallback():
      roles.append('the fallback')
    if self.isFinalizer():
      roles.append('the finalizer')
    infoSpec = """overload of function: '%s', registered as:<br><tab>%s"""
    name = self._getLatestFunc().__name__
    return textFmt(infoSpec % (name, '<br><tab>'.join(roles)))

  __repr__ = __str__
