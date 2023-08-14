"""FunctionField subclasses Constant providing a function field"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.field import Constant

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from worktoy.typetools import CallMeMaybe, Any


class FunctionField(Constant):
  """FunctionField subclasses Constant providing a function field"""

  def __init__(self, ) -> None:
    Constant.__init__(self, )

  def _explicitSetter(self, newValue: CallMeMaybe) -> None:
    if not callable(newValue, ):
      raise TypeError('Expected callable, but received %s' % type(newValue))
    Constant._explicitSetter(self, newValue)

  def __call__(self, *args, **kwargs) -> Any:
    """Passes call on to underlying function"""
    if self._value is None:
      raise TypeError('No function found!')
    return self._value(*args, **kwargs)

  def __bool__(self, ) -> bool:
    """Until the function is set, the instance returns False. After it
    returns True."""
    return False if self._value is None else True

  def setAnnotations(self, **kwargs) -> None:
    """Setter-function for annotations"""
