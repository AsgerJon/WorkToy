"""WorkToy - Wait A Minute! - ValueExistsError
This error should be raised when a variable is expected to be None when a
setter is called. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class ValueExistsError(MetaXcept):
  """WorkToy - Wait A Minute! - ValueExistsError
  This error should be raised when a variable is expected to be None when a
  setter is called. """

  def __init__(self, varName: str, existingValue: Any,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, varName, existingValue, *args, **kwargs)
    self._varName = self.pretty(varName)
    self._existingValue = self.pretty(existingValue)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    func = self.getSourceFunctionName()
    name = self._varName
    exists = self._existingValue

    msg = """Function '%s' expected variable '%s' to be 'None', but found: 
    '%s'!"""
    msg = msg % (func, name, exists)
    return '%s\n%s' % (header, self.justify(msg))
