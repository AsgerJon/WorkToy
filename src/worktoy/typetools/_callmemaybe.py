"""CallMeMaybe is a class representing callable objects"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, cast, List, TYPE_CHECKING, Any

from icecream import ic

from worktoy.core import WorkType
from worktoy.field import ListField, TypeField, Constant, FunctionField

ic.configureOutput(includeContext=True)


class CallMeMaybe(WorkType):
  """CallMeMaybe is a class representing callable objects"""

  argKey = Constant('argKey', str)
  returnKey = Constant('returnKey', str)
  argTypes = ListField()
  returnType = TypeField()
  func = FunctionField()

  @classmethod
  def __class_getitem__(cls, typeArg) -> CallMeMaybe:
    """Implementation of cursed behaviour"""
    typeArg, retType = typeArg
    out = cls(brackets=True)
    out.argTypes = cast(List[type], typeArg)
    out.returnType = cast(type, retType)
    return out

  def __init__(self, *args, **kwargs) -> None:
    if kwargs.get('brackets', None):
      return
    if kwargs.get('decorate', None):
      return

  def _decorate(self, func: CallMeMaybe) -> None:
    """Setter-function for the wrapped function"""

  def _func(self, *args, **kwargs) -> Any:
    """The function wrapped by this instance"""

  def __call__(self, *args, **kwargs) -> Any:
    """If the function field is empty the first positional argument is
    assumed to be a callable to be decorated. Otherwise, the function at
    the functionField is raised with the given arguments."""
    if self.func:
      return self.func(*args, **kwargs)
    if args:
      if callable(args[0]):
        self.func = args[0]

    raise TypeError('Expected function!')


if TYPE_CHECKING:
  CallMeMaybe = cast(Callable, CallMeMaybe)
