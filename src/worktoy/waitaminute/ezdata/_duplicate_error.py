"""
DuplicateError is raised when an 'EZData' class body assigns the same
field name twice.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from ...ezdata import EZSpace


class DuplicateError(WorkToyException, SyntaxError):
  """
  DuplicateError is raised when an EZData class body assigns the same
  field name a second time, so that one of the two declarations would
  replace the other without a word. It subclasses 'SyntaxError', as
  every refusal of a class-body line in worktoy does.

  Attributes
  ----------
  fieldName : str
    The field name the class body assigned a second time.
  space : EZSpace
    The namespace under construction; carries the class name.
  """

  __slots__ = ('fieldName', 'space')

  def __init__(self, fieldName: str, space: EZSpace) -> None:
    self.fieldName = fieldName
    self.space = space
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    infoSpec = """In the class body of 'EZData' class '%s', the already 
    existing attribute name '%s' was attempted to be defined again!"""
    clsName = self.space.getClassName()
    return textFmt(infoSpec % (clsName, self.fieldName))

  __repr__ = __str__
