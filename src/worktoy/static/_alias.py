"""
Alias allows a subclass to refer to a descriptor on the parent class with
a different name.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..waitaminute import AliasException

from . import AbstractObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
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
