"""WorkToy - Fields - Field
Basic descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from worktoy.core import Function
from worktoy.fields import AbstractField
from worktoy.sym import AccessorSym


class Field(AbstractField):
  """WorkToy - Fields - Field
  Basic descriptor implementation."""

  def __init__(self, *args, **kwargs) -> None:
    self._getterFunction = None
    self._setterFunction = None
    self._deleterFunction = None

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Wraps the inner getter function. """

  @abstractmethod
  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Wraps the inner setter function. """

  @abstractmethod
  def explicitDeleter(self, obj: object, ) -> None:
    """Wraps the inner setter function. """

  def _nameGuard(self, func: Any) -> Optional[Exception]:
    if func is not None:
      from worktoy.waitaminute import UnavailableNameException
      name = '_getterFunction'
      oldVal = self._getterFunction
      newVal = func
      return UnavailableNameException(name, oldVal, newVal)

  def _setAccessor(self, accessor: AccessorSym, func: Function) -> Function:
    pass

  def getter(self, func: Function) -> Function:
    """Decorator setting the getter function."""

  def setter(self, func: Function) -> Function:
    """Decorator setting the setter function."""

  def deleter(self, func: Function) -> Function:
    """Decorator setting the deleter function."""
