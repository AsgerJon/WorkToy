"""AbstractBox provides an abstract baseclass for descriptor protocol
implementations that automatically generate accessor methods."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AbstractDescriptor
from worktoy.waitaminute import EmptyBox

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Callable, Self, Never, Any


class AbstractBox(AbstractDescriptor):
  """AbstractBox provides an abstract baseclass for descriptor protocol
  implementations that automatically generate accessor methods."""

  def __get_existing__(self, instance: object, ) -> Any:
    """Finds an existing value in the instance's dictionary."""
    raise EmptyBox(self, instance)

  def __get_new__(self, instance: object) -> Any:
    """Generates a new value for the instance's dictionary."""
    raise NotImplementedError

  def __instance_get__(self, instance: object) -> Any:
    """The instance accessor method for the descriptor."""
    try:
      return self.__get_existing__(instance)
    except EmptyBox as emptyBox:
      return self.__get_new__(instance)
