"""
FuncOperator encapsulates a mapping from function to function,
where function is a mapping from real to real.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

from . import MathFunc

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, Union, Self, TypeAlias

  Operator: TypeAlias = Callable[[MathFunc], MathFunc]


class FuncOperator(Object):
  """FuncOperator encapsulates a mapping from function to function."""

  __func_operation__ = None

  def __init__(self, operator: Operator) -> None:
    """
    Initialize the FuncOperator with a function operator.

    :param operator: A callable that takes a MathFunc and returns a MathFunc.
    """
    self.__func_operation__ = operator

  def __call__(self, func: MathFunc) -> MathFunc:
    """
    Apply the operator to a MathFunc.

    :param func: The MathFunc to apply the operator to.
    :return: A new MathFunc that is the result of applying the operator.
    """
    return self.__func_operation__(func)
