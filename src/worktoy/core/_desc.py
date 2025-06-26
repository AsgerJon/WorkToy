"""
Desc implements the descriptor protocol for the worktoy framework.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Root, Owner, Object

if TYPE_CHECKING:
  from typing import Any


class Desc(Object):
  """
  This class attempts to solve the issue of descriptors should be able to
  return instance specific values. The problem comes from the fact that a
  nested descriptors is exposed to the owning instance only.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_owner__ = None
  __field_type__ = None

  #  Public Variables
  root = Root()
  owner = Owner()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    Returns the root of the descriptor owning the hook.
    """
    if instance is None or self.root is None:
      return self
    return self.__instance_get__()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs) -> Any:
    """
    Subclasses should implement this method to define the
    instance-specific getter. The root instance is accessed through the
    'root' attribute.
    """
    from ..waitaminute import AccessError
    raise AccessError(self)

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Subclasses should implement this method to define the
    instance-specific setter. The root instance is accessed through the
    'root' attribute.
    """
    from ..waitaminute import ReadOnlyError, AccessError
    try:
      value = self.__instance_get__()
    except AccessError as accessError:
      value = accessError
    raise ReadOnlyError(self.root, self, value)

  def __instance_del__(self, **kwargs) -> None:
    """
    Subclasses should implement this method to define the
    instance-specific deleter. The root instance is accessed through the
    'root' attribute.
    """
    from ..waitaminute import AccessError, ProtectedError
    try:
      value = self.__instance_get__()
    except AccessError as accessError:
      value = accessError
    raise ProtectedError(self.root, self, value)
