"""WorkToy - Fields - StrField
String-valued immutable field."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Function
from worktoy.fields import AbstractField


class StrField(AbstractField):
  """WorkToy - Fields - StrField
  String-valued immutable field."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)

  def getFieldSource(self) -> type:
    """Integer"""
    return str

  def getPermissionLevel(self) -> int:
    """Protected. """
    return 2

  def getDefValFactory(self, ) -> Function:
    """Getter-function for default value factory"""
    return lambda: ''
