"""
DuplicateError is raised when an 'EZData' class body assigns the same
field name twice.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from ...ezdata import EZSpace


class DuplicateError(NoPickle, AttributeError):
  """
  DuplicateError subclasses 'AttributeError' and provides a custom exception
  raised to indicate that a variable was attempted to be defined more than
  once in the same scope.

  Attributes
  ----------
  fieldName : str
    The field name the class body assigned a second time. It is not kept
    at 'name', which an 'AttributeError' reads as the name of a missing
    attribute, and which tracebacks from Python 3.12 on answer with a
    suggestion.
  space : EZSpace
    The namespace under construction; carries the class name.
  """

  __slots__ = ('fieldName', 'space')

  def __init__(self, fieldName: str, space: EZSpace) -> None:
    self.fieldName = fieldName
    self.space = space
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """In the class body of 'EZData' class '%s', the already 
    existing attribute name '%s' was attempted to be defined again!"""
    clsName = self.space.getClassName()
    return textFmt(infoSpec % (clsName, self.fieldName))

  __repr__ = __str__
