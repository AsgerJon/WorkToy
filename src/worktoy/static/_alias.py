"""
Alias allows a subclass to refer to a descriptor on the parent class with
a different name.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..waitaminute import AliasException

from . import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never


class Alias(AbstractObject):
  """
  Alias allows a subclass to refer to a descriptor on the parent class
  with a different name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __original_name__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, originalName: str) -> None:
    """
    Must be instantiated with the original name of the descriptor
    """
    super().__init__()
    self.__original_name__ = originalName

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    Set the name of the alias in the owner class.
    """
    super().__set_name__(owner, name, **kwargs)
    parentDescriptor = getattr(owner, self.__original_name__, None)
    if parentDescriptor is None:
      raise AliasException(owner, name)
    setattr(owner, name, parentDescriptor)

  def __instance_get__(self, **kwargs) -> Any:
    """
    Returns the value of the original descriptor. Please note that if
    accessed through the owning class, with instance being 'None',
    the 'Alias' object not the original object is returned.
    """
    originalDescriptor = getattr(self.owner, self.__original_name__, None)
    if originalDescriptor is None:
      raise AliasException(self.owner, self.__original_name__)
    return originalDescriptor.__get__(self.instance, self.owner, **kwargs)
