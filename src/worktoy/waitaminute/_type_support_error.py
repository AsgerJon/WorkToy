"""WorkToy - Wait A Minute! - TypeSupportError
  This exception should be raised when the argument type is not supported."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class TypeSupportError(MetaXcept):
  """WorkToy - Wait A Minute! - TypeSupportError
  This exception should be raised when the argument type is not supported."""

  def __init__(self, expectedType: type, actualValue: Any, argName: str,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._expectedType = self.pretty(expectedType)
    self._actualValue = self.pretty(actualValue)
    self._actualType = self.pretty(actualValue.__class__)
    self._argName = self.pretty(argName)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    expType = self._expectedType
    actType = self._actualType
    actVal = self._actualValue
    argName = self._argName
    funcName = self.getSourceFunctionName()
    body = """Function '%s' expected the argument: '%s' to be an instance of 
    type: '%s', but received '%s' of type '%s'!"""
    msg = body % (funcName, argName, expType, actVal, actType)
    return '%s\n%s' % (header, self.justify(msg))
