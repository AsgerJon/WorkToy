"""This module provides custom exceptions for the 'worktoy.ezdata'
package."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.meta import CallMeMaybe
from worktoy.text import monoSpace


class IllegalMethodException(TypeError):
  """This exception is raised when a subclass of EZData tries to implement
  a custom method. """

  def __init__(self, clsName: str, key: str, func: CallMeMaybe) -> None:
    e = """During class body execution for class: '%s', a custom method at 
    name: '%s' was encountered. EZData subclasses are not allowed to 
    implement methods! The function encountered was: '%s'."""
    e2 = e % (clsName, key, func)
    super().__init__(monoSpace(e2))


class IllegalInitException(IllegalMethodException):
  """This exception is raised when a subclass of EZData tries to implement
  a custom '__init__' method. """

  def __init__(self, clsName: str, func: object) -> None:
    e = """During class body execution for class: '%s', a custom '__init__'
    method was encountered. Subclasses are not allowed to implement the 
    '__init__' method! The function encountered was: %s""" % (clsName, func)
    TypeError().__init__(self, monoSpace(e))


class NoDefaultError(ValueError):
  """This exception is raised when an EZData subclass sets an AttriBox
  instance without a default value. """

  def __init__(self, clsName: str, key: str, box: AttriBox) -> None:
    e = """During class body execution for class '%s', an AttriBox 
    instance was encountered at name: '%s' having type: '%s', but no 
    default value could be found!"""
    e2 = e % (clsName, key, box)
    super().__init__(monoSpace(e2))


class AmbiguousDefaultError(ValueError):
  """This exception is raised when an EZData subclass sets an AttriBox
  instance with an ambiguous default value. """

  def __init__(self, clsName: str, key: str, box: AttriBox) -> None:
    e = """During class body execution for class '%s', an AttriBox 
    instance was encountered at name: '%s' having type: '%s', but the 
    default value is ambiguous!"""
    e2 = e % (clsName, key, box)
    super().__init__(monoSpace(e2))


class DefaultTypeMismatchError(TypeError):
  """This exception is raised when an EZData subclass sets an AttriBox
  instance with a default value of the wrong type. """

  def __init__(self,
               clsName: str,
               key: str,
               box: AttriBox,
               obj: object, ) -> None:
    attrName = key
    expType = AttriBox.getFieldClass(box).__name__
    actType = type(obj).__name__
    objStr = monoSpace(str(obj))
    e = """Attribute '%s' on class '%s' specifies type: '%s', but received 
    '%s' of type: '%s'!"""
    e2 = e % (attrName, clsName, expType, objStr, actType)
    super().__init__(monoSpace(e2))
