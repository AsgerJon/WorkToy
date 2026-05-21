"""
DuplicateError subclasses 'AttributeError' and provides a custom exception
raised to indicate that a second attribute assignment was attempted at the
same name in the same 'EZData' class body.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from ...ezdata import EZSpace


class DuplicateError(AttributeError):
  """
  DuplicateError subclasses 'AttributeError' and provides a custom exception
  raised to indicate that a variable was attempted to be defined more than
  once in the same scope.
  """

  __slots__ = ('name', 'space')

  def __init__(self, name: str, space: EZSpace) -> None:
    self.name = name
    self.space = space
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """In the class body of 'EZData' class '%s', the already 
    existing attribute name '%s' was attempted to be defined again!"""
    clsName = self.space.getClassName()
    return infoSpec % (clsName, self.name)

  __repr__ = __str__
