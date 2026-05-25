"""
Permuter subclasses 'CallMeMaybe' from 'worktoy.dispatch' and provides
an 'Arrangement' that reorders received positional arguments before
forwarding to the wrapped function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from typing import TYPE_CHECKING, overload

from ..dispatch import CallMeMaybe
from ..utilities import textFmt, QuickDesc
from ..utilities.combinatorics import Arrangement
from ..waitaminute import TypeException
from ..waitaminute.desc import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Self, Any, Union, Optional, Type

  MaybeArrangement: TypeAlias = Optional[Arrangement]
  NIType: TypeAlias = Type[NotImplemented]


class Permuter(CallMeMaybe):
  """
  Permuter subclasses 'CallMeMaybe' from 'worktoy.dispatch' and provides
  an 'Arrangement' that reorders received positional arguments before
  forwarding to the wrapped function.

  At call time, the user supplies arguments in the order described by
  'self.arrangement.values'. Before forwarding to the wrapped function,
  'arrangement.restoreFrom(*args)' permutes those arguments back into
  the canonical order described by 'self.arrangement.items'. This is
  the direction the wrapped function expects.

  Parameters
  ----------
  func: FunctionType (optional)
    The function to wrap. If not provided, it must be set by calling
    the 'setFunction' method before the 'Permuter' instance can be
    called.
  arrangement: Arrangement (optional)
    The 'Arrangement' object that specifies the reordering of received
    positional arguments. If not provided, it must be set by calling
    the 'setArrangement' method before the 'Permuter' instance can be
    called.

  The parameters may be provided positionally only but in any order.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __arg_arrangement__: MaybeArrangement = None

  #  Public Variables
  arrangement: QuickDesc[Arrangement] = QuickDesc('__arg_arrangement__')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setArrangement(self, arrangement: Arrangement) -> None:
    """Set the 'Arrangement' once. Raises 'WriteOnceError' if already
    set, 'TypeException' if not an 'Arrangement'."""
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
    """Construct a new 'Permuter' wrapping the same function as
    'original' but with a different 'Arrangement'."""
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

  def invoke(self, func: Func, *args, **kwargs) -> Any:
    """Forward to 'func' after restoring args from arranged order to
    canonical order."""
    return func(*self.arrangement.restoreFrom(*args), **kwargs)
