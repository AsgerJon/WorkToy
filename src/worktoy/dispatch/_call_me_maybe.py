"""
CallMeMaybe subclasses 'Object' from 'worktoy.core' and provides a general
function decorator that wraps the decorated function and forwards calls to
it by implementing the '__call__' method.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar
from collections.abc import Callable

from ..utilities import textFmt, QuickDesc
from ..waitaminute import MissingVariable, TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional, Union, Any, Self

T = TypeVar('T')


class _Wrapped(QuickDesc, Generic[T]):
  def __get__(self, instance: Any, owner: type) -> Union[T, Self]:
    if instance is None:
      return self
    if self.__private_key__ is None:
      raise MissingVariable(self, '__private_key__', str)
    if not isinstance(self.__private_key__, str):
      raise TypeException('__private_key__', self.__private_key__, str)
    funcTuple = getattr(instance, self.__private_key__)
    if funcTuple is None:
      raise MissingVariable(instance, self.__private_key__, tuple)
    if isinstance(funcTuple, tuple):
      return funcTuple[0]
    raise TypeException('funcTuple', funcTuple, tuple)


class CallMeMaybe:
  """
  Holds a reference to a function and forwards calls to it via '__call__'.

  This is a deliberately minimal indirection layer: a 'CallMeMaybe'
  instance wraps a single function and behaves as if calls to the
  instance were calls to the wrapped function. The wrapped function is
  stored such that the descriptor protocol does not bind it - see
  '_getWrappedFunction' for the mechanics.

  This class intentionally does not implement '__get__'. It exists for
  use as a non-descriptor callable in the 'overload.flex' machinery,
  where descriptor binding would interfere with dispatch. To enforce
  this, '__set_name__' raises 'TypeError' if a 'CallMeMaybe' instance
  is assigned as a class attribute. Use it as a free-standing object,
  not as a class member.

  Subclasses that need descriptor behaviour must override '__set_name__'
  and accept the resulting binding semantics.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __function_case__: Optional[tuple[Callable]] = None

  #  Public Variables
  __wrapped__: _Wrapped[Callable] = _Wrapped('__function_case__')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getWrappedFunction(self, ) -> Callable:
    """
    Returns the wrapped function from its single-element tuple storage.

    The wrapped function is held in '__function_case__' as a one-tuple
    '(func,)' rather than as a bare attribute. This is deliberate. Plain
    Python functions implement the descriptor protocol via 'FunctionType.
    __get__', which means that storing 'func' directly as
    'self.__function_case__ = func' would cause attribute access on a
    'CallMeMaybe' instance to bind 'func' as a method - silently
    prepending the 'CallMeMaybe' instance as the first argument the next
    time the function is invoked. The tuple wrapper is opaque to the
    descriptor protocol: a tuple's '__get__' is whatever 'object'
    inherits, i.e. nothing, so 'self.__function_case__' returns the
    tuple itself with no binding shenanigans, and indexing '[0]'
    retrieves the original function unaltered.

    The same defense is why this getter exists at all rather than
    exposing '__function_case__' directly: callers should never see the
    tuple, only the function inside it. The tuple is plumbing.
    """
    if self.__function_case__ is None:
      raise MissingVariable(self, '__function_case__', tuple)
    return self.__function_case__[0]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setFunction(self, func: Callable) -> None:
    """
    This method sets the wrapped function. The default implementation
    stores the function object in a single-element tuple thus deactivating
    the descriptor protocol on it.
    """
    self.__function_case__ = (func,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, func: Callable = None) -> None:
    if func is not None:
      if not callable(func):
        raise TypeException('func', func, Callable)
      self.setFunction(func)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, *args: Any, **kwargs: Any) -> Any:
    func = self._getWrappedFunction()
    return self.invoke(func, *args, **kwargs)

  def __set_name__(self, owner: type, name: str) -> None:
    """
    CallMeMaybe implements only the invocation of wrapped functions
    allowing for customization and enhancement. It does not provide
    descriptor protocol support. Thus, this implementation of
    '__set_name__' always raises 'TypeError' preventing accidental
    descriptor use.

    Subclasses that need descriptor behaviour must replace this method as
    class creation will invoke it and pass the following:

    Parameters
    ----------
    self : Subclass of CallMeMaybe
      The instance of the subclass instantiated in a class body.
    owner : type
      The class created by the class body
    name : str
      The name by which the instance is assigned in the class body
    """
    infoSpec = """'%s' does not support the descriptor protocol!"""
    clsName = type(self).__name__
    info = infoSpec % clsName
    raise TypeError(textFmt(info))

  def __getattr__(self, key: str) -> Any:
    if key in ('__function_case__', '__wrapped__'):
      return object.__getattribute__(self, key)
    try:
      value = getattr(self.__wrapped__, key)
    except AttributeError:
      return object.__getattribute__(self, key)
    else:
      return value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def invoke(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    This method specifies how the wrapped function object 'func' receives
    the given arguments. The default simply passes them through, leaving
    subclasses free to customize.

    Parameters
    ----------
    func : FunctionType
      The wrapped function. Provided as an explicit argument so that
      subclasses can transform, replace, or selectively invoke it
      without reaching into instance state.
    *args : Any
      Positional arguments forwarded from '__call__'.
    **kwargs : Any
      Keyword arguments forwarded from '__call__'.

    Returns
    -------
    Any
      Whatever 'func' returns, possibly transformed by the subclass.
    """
    return func(*args, **kwargs)
