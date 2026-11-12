"""
ReservedFieldError is raised when an 'EZData' class body declares a field
at a name reserved for a method of the class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from ...ezdata import EZSpace


class ReservedFieldError(WorkToyException, SyntaxError):
  """
  ReservedFieldError is raised when an EZData class body declares a
  field, an 'EZField' or a plain value, at a name that EZData reserves
  for a method of the class: the six it generates where the class has
  none of its own, 'asDict', 'asTuple', 'replace', '__field_pairs__',
  '__repr__' and '__str__', and '__post_init__', which it calls and the
  class writes. A method may be written at each of these names; only a
  field is refused. It subclasses 'SyntaxError', as every refusal of a
  class-body line in worktoy does.

  Attributes
  ----------
  fieldName : str
    The reserved name the user attempted to bind an EZField to.
  space : EZSpace
    The namespace under construction; carries the class name and
    the reserved-name list.
  """

  __slots__ = ('fieldName', 'space')

  def __init__(self, fieldName: str, space: EZSpace) -> None:
    self.fieldName = fieldName
    self.space = space
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    infoSpec = """In the class body of EZData class '%s', the name '%s'
    is reserved for a method of the class and cannot be used as a field
    name. Reserved names: %s. A method may be written at these names;
    only a field is refused."""
    clsName = self.space.getClassName()
    reserved = ', '.join(
        repr(n) for n in self.space.__reserved_ez_names__
    )
    info = infoSpec % (clsName, self.fieldName, reserved)
    return textFmt(info)

  __repr__ = __str__
