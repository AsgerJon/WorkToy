"""WorkSide - Wait A Minute! - UnavailableName
Exception raised when a name is already occupied."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class UnavailableNameException(MetaXcept):
  """WorkSide - Wait A Minute! - UnavailableName
  Exception raised when a name is already occupied."""

  def __init__(self, name: str, oldVal: Any, newVal: Any,
               *args, **kwargs) -> None:
    self._name = name
    self._oldVal = oldVal
    self._newVal = newVal

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    func = self.getFuncQualName()
    newVal = self._newVal
    name = self._name
    oldVal = self._oldVal
    msg = """Function '%s' attempted to assign new value: '%s' to name: 
    '%s' which is already populated with: '%s'!"""
    body = msg % (func, newVal, name, oldVal)
    return self.monoSpace('<br>'.join([header, body]))
