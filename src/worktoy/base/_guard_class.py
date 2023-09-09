"""WorkToy - Base - GuardClass
Provides guard methods to the DefaultClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.base import CoreClass
from worktoy.core import Function


class GuardClass(CoreClass):
  """WorkToy - Base - GuardClass
  Provides guard methods to the DefaultClass"""

  def __init__(self, *args, **kwargs) -> None:
    CoreClass.__init__(self, *args, **kwargs)

  def noneGuard(self, obj: object, varName: str = None) -> Any:
    """Raises error if given object is not None."""
    if obj is not None:
      from worktoy.waitaminute import UnavailableNameException
      raise UnavailableNameException(self.maybe(varName, 'obj'), obj)

  def someGuard(self, obj: object, varName: str = None) -> Any:
    """Raises error if given object is None."""
    if obj is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError(self.maybe(varName, 'obj'))
    return obj

  def functionGuard(self, func: Function, name: str = None) -> Function:
    """Raises error if given object is not a function."""
    argName = self.maybe(name, 'func')
    if not callable(self.someGuard(func, argName)):
      from worktoy.waitaminute import TypeSupportError
      expectedType = Function
      actualValue = func
      raise TypeSupportError(expectedType, actualValue, argName)
    return func

  def intGuard(self, integer: int, name: str = None) -> int:
    """Raises error if given object is None or not an integer."""
    argName = self.maybe(name, 'integer')
    if not isinstance(self.someGuard(integer), int):
      from worktoy.waitaminute import TypeSupportError
      expectedType = int
      actualValue = integer
      raise TypeSupportError(expectedType, actualValue, argName)
    return integer

  def floatGuard(self, value: int, name: str = None) -> int:
    """Raises error if given object is None or not a float."""
    argName = self.maybe(name, 'float')
    if not isinstance(self.someGuard(value), (int, float)):
      from worktoy.waitaminute import TypeSupportError
      expectedType = float
      actualValue = value
      raise TypeSupportError(expectedType, actualValue, argName)
    return value

  def strGuard(self, value: str, name: str = None) -> str:
    """Raises error if given object is None or not a string."""
    argName = self.maybe(name, 'text')
    if not isinstance(self.someGuard(value), str):
      from worktoy.waitaminute import TypeSupportError
      expectedType = str
      actualValue = value
      raise TypeSupportError(expectedType, actualValue, argName)
    return value
