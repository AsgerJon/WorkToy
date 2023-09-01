"""WorkToy - Fields - ReadOnlyDescriptor
Subclass of AbstractDescriptor explicitly read-only."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from worktoy.fields import AbstractDescriptor


class ReadOnlyDescriptor(AbstractDescriptor):
  """WorkToy - Fields - ReadOnlyDescriptor
  Subclass of AbstractDescriptor explicitly read-only."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)

  def getPermissionLevel(self) -> int:
    """Always 1"""
    return 1

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function. Subclasses must implement this method."""
    return self.illegalSetter(obj, newValue)

  def explicitDeleter(self, obj: object, ) -> None:
    """Explicit deleter function. Subclasses must implement this method."""
    return self.illegalDeleter(obj, )

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Explicit getter function. Subclasses must implement this method."""
