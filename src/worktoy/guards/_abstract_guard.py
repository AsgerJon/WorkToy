"""WorkToy - Guard - AbstractGuard
Abstract baseclass for the Guard classes. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from worktoy.fields import ReadOnlyDescriptor
from worktoy.guards import MetaGuard


class AbstractGuard(ReadOnlyDescriptor, metaclass=MetaGuard):
  """WorkToy - Guard - AbstractGuard
  Abstract baseclass for the Guard classes. """

  def __init__(self, *args, **kwargs) -> None:
    ReadOnlyDescriptor.__init__(self, *args, **kwargs)
    self._fieldName = None
    self._fieldOwner = None

  @abstractmethod
  def validate(self, obj: Any, name: str) -> Any:
    """Responsible for validating the obj."""

  @abstractmethod
  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Subclasses must implement this method."""

  def __set_name__(self, cls: type, name: str) -> None:
    self._fieldName = name
    self._fieldOwner = cls
