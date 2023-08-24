"""WorkToy - ExceptionFactory
This module provides factories for custom exception classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import ParsingClass, Function


class ExceptionClass(ParsingClass):
  """WorkToy - ExceptionFactory
  This module provides factories for custom exception classes."""

  def __init__(self, *args, **kwargs) -> None:
    ParsingClass.__init__(self, *args, **kwargs)

  def createException(self, name: str, nameSpace: dict = None) -> type:
    """Creates and exception type with given name and msg"""
    bases = (Exception,)
    return type(name, bases, nameSpace)

  def createUnexpectedTypeException(self, *args, ) -> type:
    """Creates the UnexpectedTypeException"""
    expType, actType = self.maybeTypes(type, *args, pad=2)
    msg = """Expected type %s but received %s""" % (expType, actType)
    name = 'UnexpectedTypeException'
    return type(name, (Exception,), {})(msg)
