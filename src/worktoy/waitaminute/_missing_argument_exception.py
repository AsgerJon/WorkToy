"""WorkToy - Wait A Minute! - MissingArgumentException
This exception should be raised when a function is missing a required
argument."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class MissingArgumentException(MetaXcept):
  """WorkToy - Wait A Minute! - UnexpectedStateError
  Invoked when a function is called before it is ready."""

  def __init__(self, missingArgument: str, *args, **kwargs) -> None:
    MetaXcept.__init__(self, missingArgument, *args, **kwargs)
    self._missingArgument = self.pretty(missingArgument)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    misArg = self._missingArgument
    funcName = self.getSourceFunctionName()
    msg = """Variable: '%s' is required for function: '%s' is missing!"""
    body = msg % (misArg, funcName)
    return '%s\n%s' % (header, self.justify(body))
