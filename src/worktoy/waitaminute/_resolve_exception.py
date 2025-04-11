"""ResolveException should be raised by classes that try to resolve
'other' objects in custom implementation of certain dunder methods. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class ResolveException(Exception):
  """ResolveException should be raised by classes that try to resolve
  'other' objects in custom implementation of certain dunder methods. """

  __self_class__ = None
  __other_object__ = None

  def __init__(self, self_: object, other: object) -> None:
    """Initialize the ResolveException object."""
    self.__self_class__ = type(self_)
    self.__other_object__ = other
    clsName = self.__self_class__.__name__
    otherStr = repr(other)
    info = """Unable to resolve '%s' as an object of type: '%s'"""
    Exception.__init__(self, info % (otherStr, clsName))
