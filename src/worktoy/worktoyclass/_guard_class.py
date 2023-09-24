"""WorkToy - Base - GuardClass
Provides guard methods to the DefaultClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Optional

from worktoy.worktoyclass import CoreClass

Function = (type(getattr(type('_', (), {'_': lambda self: self}), '_')))


class GuardClass(CoreClass):
  """WorkToy - Base - GuardClass
  Provides guard methods to the DefaultClass"""

  def __init__(self, *args, **kwargs) -> None:
    CoreClass.__init__(self, *args, **kwargs)

  def noneGuard(self, obj: object, varName: str = None) -> bool:
    """Raises UnavailableNameException if the given object is not None. """
    if obj is not None:
      from worktoy.waitaminute import UnavailableNameException
      raise UnavailableNameException(self.maybe(varName, 'obj'), obj)
    return True

  def someGuard(self, obj: Any, varName: str = None) -> Any:
    """Raises error if given object is None."""
    if obj is None:
      from worktoy.waitaminute import MissingArgumentException
      raise MissingArgumentException(self.maybe(varName, 'obj'))
    return obj

  def overRideGuard(self, obj: Any, varName: str, newValue: Any) -> Any:
    """Raises error if given object is not None. """
    if obj is not None:
      from worktoy.waitaminute import UnavailableNameException
      name = varName
      oldVal = obj
      newVal = newValue
      raise UnavailableNameException(name, oldVal, newVal)

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

  def strGuard(self, value: str, name: str = None,
               **kwargs) -> Optional[str]:
    """Raises error if given object is None or not a string."""
    if value is None:
      if not self.searchKey('allowNone', 'allow_none', **kwargs):
        from worktoy.waitaminute import MissingArgumentException
        raise MissingArgumentException(self.maybe(name, 'obj'))
      return
    argName = self.maybe(name, 'text')
    if not isinstance(self.someGuard(value), str):
      from worktoy.waitaminute import TypeSupportError
      expectedType = str
      actualValue = value
      raise TypeSupportError(expectedType, actualValue, argName)
    return value

  def createGet(self, creator: Function, name: str, **kwargs) -> Any:
    """Creator-getter recursion guard"""
    value = getattr(self, name, None)
    if value is None:
      if kwargs.get('_recursion', False):
        from worktoy.waitaminute import RecursiveCreateGetError
        raise RecursiveCreateGetError(creator, object, name)
      creator()
      return self.createGet(creator, name, recursion=True)
    return getattr(self, name, )

  @staticmethod
  def decodeStr(data: str) -> str:
    """Returns the string as is"""
    return data
