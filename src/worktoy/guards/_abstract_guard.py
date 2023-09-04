"""WorkToy - Guard - AbstractGuard
Abstract baseclass for the Guard classes. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from worktoy.core import Function
from worktoy.fields import AbstractField


class AbstractGuard(AbstractField):
  """WorkToy - Guard - AbstractGuard
  Abstract baseclass for the Guard classes. """

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, self.__guard_validator_factory__,
                           *args, **kwargs)
    self._defaultValue = self.__guard_validator_factory__
    self._fieldSource = Function
    self._fieldName = None
    self._fieldOwner = None

  @abstractmethod
  def __guard_validator_factory__(self, obj: Any, cls: type) -> Any:
    """Responsible for validating the obj."""

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Subclasses must implement this method."""
    return self.__guard_validator_factory__(obj, cls)

  def __set_name__(self, cls: type, name: str) -> None:
    self._fieldName = name
    self._fieldOwner = cls
