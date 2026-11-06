"""
CallMeMaybe wraps a function and forwards calls to it through '__call__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar
from collections.abc import Callable

from ..utilities import textFmt, QuickDesc
from ..waitaminute import MissingVariable, TypeException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Optional, Union, Any, Self

T = TypeVar('T')


class _Wrapped(QuickDesc, Generic[T]):
  """
  'CallMeMaybe.__wrapped__' must give the function a holder forwards to,
  read-only, and without the function being bound as a method on the
  way.

  Implementation
  --------------

  The function is stored in a one-element tuple, which the descriptor
  protocol leaves alone, and this descriptor returns its element. Writes
  and deletions are refused, as for every 'QuickDesc'.
  """

  def __get__(self, instance: Any, owner: type) -> Union[T, Self]:
    if instance is None:
      return self
    if self.__private_key__ is None:
      raise MissingVariable(self, '__private_key__', str)
    if not isinstance(self.__private_key__, str):
      raise TypeException('__private_key__', self.__private_key__, str)
    funcTuple = object.__getattribute__(instance, self.__private_key__)
    if funcTuple is None:
      raise MissingVariable(instance, self.__private_key__, tuple)
    if isinstance(funcTuple, tuple):
      return funcTuple[0]
    raise TypeException('funcTuple', funcTuple, tuple)


class CallMeMaybe:
  """
  The dispatch machinery needs to hold functions as plain callables:
  calling the holder calls the function, reading a name such as
  '__name__' off it reads the function's, and nothing ever binds the
  function as a method, which would hand it the holder as its first
  argument. A subclass must be able to change how the call reaches the
  function, as 'Permuter' reorders the arguments.

  Implementation
  --------------

  The function is kept as a one-element tuple, which the descriptor
  protocol does not bind, and '__wrapped__' gives it back. '__call__'
  passes the function and the arguments to 'invoke', which a subclass
  reimplements. '__getattr__' reads a missing name off the function, so
  '__name__' and '__qualname__' are the function's while '__doc__' and
  '__module__', which the class holds, are not. The holder has no
  '__get__', and '__set_name__' refuses a place in a class body; a
  subclass meant for one reimplements it and accepts the binding.

  Attributes
  ----------

  __wrapped__ : Callable
    The function held, read-only.

  __function_case__ : tuple or None
    The one-element tuple holding the function.
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
    if self.__function_case__ is None:
      raise MissingVariable(self, '__function_case__', tuple)
    return self.__function_case__[0]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setFunction(self, func: Callable) -> None:
    """
    A holder created empty must be able to receive its function later.

    Implementation
    --------------

    The function is stored as a one-element tuple, replacing any held
    before. Unlike the constructor, nothing checks that it is callable.

    Parameters
    ----------

    func : Callable
      The function to hold.
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

  def __call__(self, *args, **kwargs) -> Any:
    func = self._getWrappedFunction()
    return self.invoke(func, *args, **kwargs)

  def __set_name__(self, owner: type, name: str) -> None:
    """
    A holder placed in a class body would be a callable the class never
    binds, which is rarely what the body means.

    Implementation
    --------------

    The placement is refused. On Python 3.7 to 3.11 the refusal reaches the
    class statement wrapped in a 'RuntimeError'.

    Parameters
    ----------

    owner : type
      The class being created.

    name : str
      The name the holder was bound to.

    Raises
    ------

    TypeError
      Always.
    """
    infoSpec = """'%s' does not support the descriptor protocol!"""
    clsName = type(self).__name__
    info = infoSpec % clsName
    raise TypeError(textFmt(info))

  def __getattr__(self, key: str) -> Any:
    """
    A holder must pass for the function it holds where code reads a name
    such as '__name__' off it, yet never recurse when it holds nothing.

    Implementation
    --------------

    '__function_case__' and '__wrapped__' go to 'object.__getattribute__',
    which re-raises the 'MissingVariable' of an empty holder. Any other
    name is read off the function, and a name the function lacks raises
    from the holder.

    Parameters
    ----------

    key : str
      The missing name.

    Returns
    -------

    Any
      The value on the function.

    Raises
    ------

    AttributeError
      Neither the holder nor the function has the name.
    """
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

  def invoke(self, *args, **kwargs) -> Any:
    """
    A subclass must be able to transform, replace or skip the function on
    the way, without reaching into the holder for it, and a keyword of the
    caller named 'func' must still reach the function.

    Implementation
    --------------

    The function arrives first among the positional arguments, not as a
    named parameter. The default calls it with the rest unchanged.

    Parameters
    ----------

    *args
      The function, then the positional arguments of the call.

    **kwargs
      The keyword arguments of the call.

    Returns
    -------

    Any
      What the function returns.
    """
    func, args = args[0], args[1:]
    return func(*args, **kwargs)
