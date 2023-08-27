"""WorkToy - ExceptionFactory
This module provides factories for custom exception classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import StringAware


class ExceptionClass(StringAware):
  """WorkToy - ExceptionFactory
  This module provides factories for custom exception classes."""

  def __init__(self, *args, **kwargs) -> None:
    StringAware.__init__(self, *args, **kwargs)

  def createException(self,
                      name: str,
                      nameSpace: dict = None,
                      *_, **kwargs) -> type:
    """Creates and exception type with given name and msg"""
    return type(name, (Exception,), {**kwargs, **nameSpace})

  def createUnexpectedTypeException(self, *args, ) -> type:
    """Creates the UnexpectedTypeException.
    Give as positional arguments the expected type and then the actual
    type."""
    name = 'UnexpectedTypeException'
    expType, actType = self.maybeTypes(type, *args, pad=2)
    msg = """Expected type %s but received %s""" % (expType, actType)
    return type(name, (Exception,), {})(msg)

  def createUnexpectedStateError(self, *args, **kwargs) -> type:
    """Creates the UnexpectedStateError.
    This exception should be raised when a function is invoked before
    certain variables have been initialised. Typically, this would be when
    a variable is 'None' indicating events occurring in an unexpected
    order. Without custom exception, a 'TypeError' is commonly raised in
    this case, and the 'UnexpectedStateError' is intended as a more
    informative alternative.

    For each variable include name in function definition, expected type
    and the actual value received."""
    name = 'UnexpectedStateException'
    argumentName = None

  def createMissingFunction(self, *args, **kwargs) -> type:
    """Creates the MissingFunctionError
    This exception should be raised when a function is invoked before it
    is available. Arguments:
      'functionName: Name of the function.'
      'scope: Method or function where error was encountered.'
      'signature: The annotations of the expected function'
    """
    name = 'MissingFunctionError'
    functionName = self.maybeType(str, *args)
    scope = None
    signature = None
