"""
The 'overload' function provides a decorator setting type signatures for
particular function overload. This overloading implementation requires
that the owning class is derived from 'BaseMeta' or a subclass of
'BaseMeta'. Other classes must use the 'Dispatcher' descriptor from
'worktoy.dispatch' instead.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.dispatch import Dispatcher, TypeSig

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias
  from . import Overload

  Method: TypeAlias = Callable[..., Any]
  Decorator: TypeAlias = Callable[[Method], Overload]


class Overload:
  """
  Entry collected by LoadSpaceHook
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __type_sig__ = None
  __func_object__ = None

  #  Public Variables
  sig = Field()
  func = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @sig.GET
  def _getSig(self) -> TypeSig:
    return self.__type_sig__

  @func.GET
  def _getFunc(self) -> Method:
    return self.__func_object__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, sig: TypeSig, func: Method) -> None:
    """
    Initialize the _Overload instance with a type signature and a function.
    """
    self.__type_sig__ = sig
    self.__func_object__ = func


def overload(*types, ) -> Decorator:
  """
  The 'overload' function provides a decorator setting type signatures for
  particular function overload. This overloading implementation requires
  that the owning class is derived from 'BaseMeta' or a subclass of
  'BaseMeta'. Other classes must use the 'Dispatcher' descriptor from
  'worktoy.dispatch' instead.
  """

  sig = TypeSig(*types)

  def decorator(arg: Any) -> Overload:
    return Overload(sig, arg)

  return decorator
