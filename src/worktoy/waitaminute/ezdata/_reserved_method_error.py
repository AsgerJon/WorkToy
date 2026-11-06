"""
ReservedMethodError is raised when an 'EZData' class body defines a
method that 'EZData' generates and does not allow to be replaced.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from ...ezdata import EZSpace


class ReservedMethodError(WorkToyException, SyntaxError):
  """
  ReservedMethodError is raised when an EZData class body defines a
  method that EZData generates for every class and keeps for itself:
  '__init__', '__iter__', '__len__',
  '__eq__', '__hash__', the four ordering methods, '__setattr__' and
  '__delattr__', whether the body defines it plainly or overloads it
  with '@overload'. EZData installs these after the class body, so a
  class-body definition would be dropped without a word; the
  construction, the assignment and the deletion guard the rule that
  every field holds a value of its declared type, iteration and length
  both run over the fields, and equality, hashing and ordering all
  compare the field values; validation and derived state belong in
  '__post_init__'. A plain base, one not built by 'EZMeta', may
  define these methods, as a mixin written against the same protocol
  does; the generated methods take precedence over them. It subclasses
  'SyntaxError', as every refusal of a class-body line in worktoy does.

  Attributes
  ----------
  methodName : str
    The reserved method name the class body defined.
  space : EZSpace
    The namespace under construction; carries the class name and the
    reserved-method list.
  """

  __slots__ = ('methodName', 'space')

  def __init__(self, methodName: str, space: EZSpace) -> None:
    self.methodName = methodName
    self.space = space
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    infoSpec = """The class body of EZData class '%s' defines '%s', which
    EZData generates itself and does not allow to be replaced. Validation
    and derived state belong in '__post_init__'; equality, hashing and
    ordering compare the field values."""
    info = infoSpec % (self.space.getClassName(), self.methodName)
    return textFmt(info)

  __repr__ = __str__
