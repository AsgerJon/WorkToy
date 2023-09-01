"""WorkToy - Fields - AbstractDescriptor
Provides the implementation of the descriptor functionality. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never, Any

from icecream import ic

from worktoy.base import DefaultClass

ic.configureOutput(includeContext=True)


class AbstractDescriptor(DefaultClass, ):
  """WorkToy - Fields - AbstractDescriptor
  Provides the implementation of the descriptor functionality. """

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._permissionLevel = None

  def __get__(self, obj: object, cls: type) -> Any:
    """Getter."""
    if self.getPermissionLevel() > 0:
      return self.explicitGetter(obj, cls)
    return self.illegalGetter(obj, cls)

  def __set__(self, obj: object, newValue: object) -> None:
    """Setter."""
    if self.getPermissionLevel() > 1:
      return self.explicitSetter(obj, newValue)
    return self.illegalSetter(obj, newValue)

  def __delete__(self, obj: object, ) -> None:
    """Deleter."""
    if self.getPermissionLevel() > 2:
      return self.explicitDeleter(obj, )
    return self.illegalDeleter(obj, )

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Explicit getter function. Subclasses must implement this method."""

  @abstractmethod
  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Explicit setter function. Subclasses must implement this method."""

  @abstractmethod
  def explicitDeleter(self, obj: object, ) -> None:
    """Explicit deleter function. Subclasses must implement this method."""

  def illegalGetter(self, obj: object, cls: type) -> Never:
    """Illegal getter invoked by __get__ because of insufficient
    permission levels. """
    from worktoy.waitaminute import SecretFieldError
    raise SecretFieldError(self, obj, cls)

  def illegalSetter(self, obj: object, newValue: object) -> Never:
    """Illegal getter invoked by __set__ because of insufficient
    permission levels. """
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError(self, obj, newValue)

  def illegalDeleter(self, obj: object, ) -> Never:
    """Illegal getter invoked by __delete__ because of insufficient
    permission levels. """
    from worktoy.waitaminute import ProtectedFieldError
    raise ProtectedFieldError(self, obj)

  def getPermissionLevel(self) -> int:
    """Getter-function for permission level."""
    out = self.maybe(self._permissionLevel, 3)
    if isinstance(out, int):
      return out
