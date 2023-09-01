"""WorkToy - Wait A Minute! - RecursiveCreateGetError
Raised when a getter function calls a creator function a second time. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Function
from worktoy.waitaminute import MetaXcept


class RecursiveCreateGetError(MetaXcept):
  """WorkToy - Wait A Minute! - RecursiveCreateGetError
  Raised when a getter function calls a creator function a second time. """

  def __init__(self, creator: Function, varType, varName: str,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, creator, varType, varName, *args, **kwargs)
    self._creator = self.pretty(creator)
    self._varType = self.pretty(varType)
    self._varName = self.pretty(varName)

  def __str__(self) -> str:
    header = MetaXcept.__str__(self)
    creator = self._creator
    varType, varName = self._varType, self._varName
    getter = self.getSourceFunctionName()
    msg = """Recursive behaviour detected between creator function: '%s' and 
    getter function '%s' for the variable: '%s: %s'."""
    msg = msg % (creator, getter, varName, varType)
    return '%s\n%s' % (header, self.justify(msg))
