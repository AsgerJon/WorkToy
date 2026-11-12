"""
DuplicateError is raised when an 'EZData' class body binds a name twice
and one of the two bindings is a field.
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
  DuplicateError is raised when an EZData class body binds a name it
  bound before and one of the two bindings is a field: a field bound a
  second time, a field bound at the name of a method or a descriptor of
  the body, or a method or a descriptor bound at the name of a field.
  One of the two declarations would otherwise replace or hide the other
  without a word. A body binding a method, a descriptor or an overload at
  the name of a field the class inherits shows that name bound once, so
  for it the message adds that the name is an inherited field. It
  subclasses 'SyntaxError', as every refusal of a class-body line in
  worktoy does.

  Attributes
  ----------
  fieldName : str
    The name the class body bound a second time.
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
    info = infoSpec % (clsName, self.fieldName)
    inherited = self.fieldName in self.space.getBaseFields()
    declared = self.fieldName in self.space.getEZFields()
    if inherited and not declared:
      #  This branch is reached by the following:
      #  - The body binds a method, a descriptor or an overload at the
      #    name of a field the class inherits and does not declare again,
      #    so the body itself shows the name bound once
      infoSpec = """%s '%s' is a field the class inherits, and the name
      of a field can only be declared again as a field."""
      info = infoSpec % (info, self.fieldName)
    #  The rest of the method is reached by every refusal.
    return textFmt(info)

  __repr__ = __str__
