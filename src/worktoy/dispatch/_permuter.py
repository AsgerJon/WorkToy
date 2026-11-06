"""
Permuter reorders positional arguments before forwarding them to the
wrapped function.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from typing import TYPE_CHECKING, overload

from ..utilities import textFmt, QuickDesc
from ..utilities.combinatorics import Arrangement
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import WriteOnceError
from . import CallMeMaybe

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Self, Any, Union, Optional, Type

  MaybeArrangement: TypeAlias = Optional[Arrangement]
  NIType: TypeAlias = Type[NotImplemented]


class Permuter(CallMeMaybe):
  """
  An overload declared with 'overload.flex(str, int)' must accept its
  arguments in any order, '(str, int)' as well as '(int, str)', while the
  function itself declares them in one order. Each accepted order needs a
  callable that puts the arguments back in the declared order before
  calling the function.

  Implementation
  --------------

  A 'Permuter' holds the function and an 'Arrangement'. A caller gives
  the arguments in the order of 'arrangement.values', and
  'arrangement.restoreFrom' puts them back in the order of
  'arrangement.items', the order of the parameters. Keywords pass
  unchanged. The constructor takes a plain function and an arrangement,
  each optional, positionally and in either order. 'p << arrangement'
  and 'arrangement >> p' give a new 'Permuter' over the same function,
  and 'p <<= arrangement' sets the arrangement once in place.

  Attributes
  ----------

  arrangement : Arrangement
    The arrangement, read-only.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __arg_arrangement__: MaybeArrangement = None

  #  Public Variables
  arrangement: QuickDesc[Arrangement] = QuickDesc('__arg_arrangement__')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getArrangement(self) -> Arrangement:
    if self.__arg_arrangement__ is None:
      raise MissingVariable(self, '__arg_arrangement__', Arrangement)
    return self.__arg_arrangement__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setArrangement(self, arrangement: Arrangement) -> None:
    """
    A 'Permuter' created without an arrangement must receive one later,
    once, since a 'Permuter' changing its order after dispatch was built
    would silently reroute calls.

    Parameters
    ----------

    arrangement : Arrangement
      The order the caller gives the arguments in.

    Raises
    ------

    TypeException
      'arrangement' is not an 'Arrangement'.

    WriteOnceError
      An arrangement is set already.
    """
    if not isinstance(arrangement, Arrangement):
      raise TypeException('arrangement', arrangement, Arrangement)
    if self.__arg_arrangement__ is not None:
      raise WriteOnceError(self, self.__arg_arrangement__, arrangement)
    self.__arg_arrangement__ = arrangement

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  @overload
  def __init__(self, ) -> None: ...
  @overload
  def __init__(self, func: Func) -> None: ...
  @overload
  def __init__(self, arrangement: Arrangement) -> None: ...
  @overload
  def __init__(self, func: Func, arrangement: Arrangement) -> None: ...
  @overload
  def __init__(self, arrangement: Arrangement, func: Func) -> None: ...
  # @formatter:on

  def __init__(self, *args) -> None:
    if len(args) > 2:
      infoSpec = """'%s' constructor accepts at most two positional
      arguments, but received '%d':<br><tab>%s"""
      clsName: str = type(self).__name__
      argStr: str = '<br><tab>'.join(str(arg) for arg in args)
      n: int = len(args)
      info: str = infoSpec % (clsName, n, argStr)
      raise ValueError(textFmt(info))
    _func, _arrangement = None, None
    for arg in args:
      if isinstance(arg, Arrangement):
        if _arrangement is None:
          _arrangement = arg
        else:
          infoSpec = """'%s' constructor expects at most one
          'Arrangement' object, but received:
          <br><tab>%s<br><tab>%s"""
          clsName: str = type(self).__name__
          arrStr: str = str(_arrangement)
          argStr: str = str(arg)
          info: str = infoSpec % (clsName, arrStr, argStr)
          raise ValueError(textFmt(info))
      elif isinstance(arg, Func):
        if _func is None:
          _func = arg
        else:
          infoSpec = """'%s' constructor expects at most one
          'FunctionType' object, but received:
          <br><tab>%s<br><tab>%s"""
          clsName: str = type(self).__name__
          funcStr: str = str(_func)
          argStr: str = str(arg)
          info: str = infoSpec % (clsName, funcStr, argStr)
          raise ValueError(textFmt(info))
      else:
        raise TypeException('arg', arg, Arrangement, Func)
    super().__init__(_func)
    if _arrangement is not None:
      self.setArrangement(_arrangement)

  @classmethod
  def newArrangement(
      cls, original: Self, arrangement: Arrangement,
  ) -> Self:
    """
    Each order of a flexible declaration needs its own 'Permuter' over the
    same function.

    Parameters
    ----------

    original : Permuter
      The 'Permuter' whose function is reused.

    arrangement : Arrangement
      The arrangement of the new 'Permuter'.

    Returns
    -------

    Permuter
      A new instance of the class it is called on.
    """
    return cls(original.__wrapped__, arrangement)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __lshift__(self, arrangement: Arrangement) -> Union[NIType, Self]:
    if isinstance(arrangement, Arrangement):
      cls = type(self)
      return cls.newArrangement(self, arrangement)
    return NotImplemented

  def __ilshift__(self, arrangement: Arrangement) -> Union[NIType, Self]:
    if isinstance(arrangement, Arrangement):
      self.setArrangement(arrangement)
      return self
    return NotImplemented

  def __rrshift__(self, arrangement: Arrangement) -> Union[NIType, Self]:
    return self << arrangement

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def invoke(self, *args, **kwargs) -> Any:
    """
    The function must receive its positional arguments in the order it
    declares them, whatever order the caller used.

    Implementation
    --------------

    The arguments after the function are restored through the
    arrangement; keywords pass unchanged. A caller keyword named 'func'
    reaches the function, as in 'CallMeMaybe.invoke'.

    Parameters
    ----------

    *args
      The function, then the positional arguments in the order of
      'arrangement.values'.

    **kwargs
      Keyword arguments.

    Returns
    -------

    Any
      What the function returns.

    Raises
    ------

    ValueError
      The number of positional arguments differs from the length of the
      arrangement.
    """
    func, args = args[0], args[1:]
    return func(*self._getArrangement().restoreFrom(*args), **kwargs)
