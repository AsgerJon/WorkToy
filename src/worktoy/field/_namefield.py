"""NameField subclasses Constant requiring a string."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.field import Constant, PermissionLevel


class NameField(Constant):
  """NameField subclasses Constant requiring a string."""

  @classmethod
  def _getPermissionLevel(cls) -> PermissionLevel:
    """Implementation returning read only permission"""
    return PermissionLevel.READ_ONLY

  def __init__(self, name: str = None) -> None:
    Constant.__init__(self)
    if name is not None:
      self._value = name
