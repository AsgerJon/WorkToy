"""WorkToy - Wait A Minute! - UnexpectedStateError
Invoked when a function is called before it is ready."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class UnexpectedStateError(MetaXcept):
  """WorkToy - Wait A Minute! - UnexpectedStateError
  Invoked when a function is called before it is ready."""

  def __init__(self, missingVariable: str, *args, **kwargs) -> None:
    MetaXcept.__init__(self, missingVariable, *args, **kwargs)
    self._missingVariable = self.pretty(missingVariable)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    misVar = self._missingVariable
    funcName = self.getSourceFunctionName()
    msg = """Variable: '%s' is required for function: '%s', but is 'None'!"""
    body = msg % (misVar, funcName)
    return '%s\n%s' % (header, self.justify(body))
