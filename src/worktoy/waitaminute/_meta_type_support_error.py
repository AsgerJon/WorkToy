"""WorkToy - Wait A Minute! - MetaTypeSupportError
Indicates that an instance is not a member of class derived from the
correct metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class MetaTypeSupportError(MetaXcept):
  """WorkToy - Wait A Minute! - MetaTypeSupportError
  Indicates that an instance is not a member of class derived from the
  correct metaclass."""

  def __init__(self, expMetaClass: type, actualValue: Any, argName: str,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, expMetaClass, actualValue, argName)
    self._expMetaClass = self.pretty(expMetaClass)
    self._actualValue = self.pretty(actualValue)
    self._actualType = self.pretty(actualValue.__class__)
    self._actualMetaClass = self.pretty(self._actualType.__class__)
    self._argName = self.pretty(argName)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    expMcls = self._expMetaClass
    actVal = self._actualValue
    actCls = self._actualType
    actMcls = self._actualMetaClass
    argName = self._argName
    funcName = self.getSourceFunctionName()
    body = """Function '%s' expected the argument: '%s' to be an instance of 
    a class derived from metaclass: '%s', but '%s' belongs to class: '%s' 
    which is derived from '%s'."""
    msg = body % (funcName, argName, actMcls, argName, actCls, actMcls)

    return '%s\n%s' % (header, self.justify(msg))
