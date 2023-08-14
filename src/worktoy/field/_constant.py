"""Constant subclasses Field to provide a simplified version when fields
of constant value are intended. The constructor expects the first
positional argument to hold the value to be retained throughout the
existence of the instance. The type is inferred automatically."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.field import PermissionLevel, BaseField

ic.configureOutput(includeContext=True)


class Constant(BaseField):
  """Constant subclasses Field to provide a simplified version when fields
  of constant value are intended."""

  @classmethod
  def _getPermissionLevel(cls) -> PermissionLevel:
    """Implementation returning read only permission"""
    return PermissionLevel.READ_ONLY

  def __init__(self, *args, **kwargs) -> None:
    BaseField.__init__(self, *args, **kwargs)
