"""
ArgumentException provides a custom exception raised when a function is
unable to parse received arguments.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, TypeAlias


class ArgumentException(ValueError):
  """
  ArgumentException provides a custom exception raised when a function is
  unable to parse received arguments.
  """

  posArgs = _Attribute()
  keyArgs = _Attribute()
  func = _Attribute()

  def __init__(self, func: Func, *args: Any, **kwargs) -> None:
    self.posArgs = [*args, ]
    self.keyArgs = {**kwargs, }
    self.func = func
    ValueError.__init__(self, 'unable to parse arguments!')
