"""Testing extractArg"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, TypeAlias, Any
from unittest import TestCase
import inspect
import inspect

ARG: TypeAlias = tuple[Any, ...]
RETURN: TypeAlias = tuple[Any, ...]


def invFmt(methodName, *args, **kwargs):
  """Formats the invocation code in a human-readable format.
  Args:
      methodName (str): The name of the method.
      *args: Variable positional arguments.
      **kwargs: Variable keyword arguments.
  Returns:
      str: Formatted invocation code."""
  formattedArgs = [formatValue(arg) for arg in args]
  formattedKwargs = [
    "%s=%s" % (key, formatValue(value)) for key, value in kwargs.items()]
  allArgs = formattedArgs + formattedKwargs
  invocation = "%s(%s)" % (methodName, ', '.join(allArgs))
  return invocation


def formatValue(value):
  """Formats the value representation based on its type.
  Args:
      value: The value to be formatted.
  Returns:
      str: Formatted value representation."""
  if inspect.isclass(value):
    return "%s" % value.__name__
  elif inspect.isfunction(value):
    return "%s" % value.__name__
  elif isinstance(value, str):
    return "'%s'" % value
  else:
    return "%r" % value


class TestExtractArgs(TestCase):
  """Fuck unittests"""

  def unstupid(self, inCode: str, inArg: ARG, expec: RETURN, ) -> NoReturn:
    """Since the normal unittests are so bad, this function might make it
    better"""

  def testArgs(self, ) -> NoReturn:
    """Here we test simple positional matches"""
