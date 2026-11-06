"""
OverloadReference is raised when a reference through 'THIS' names an
overloaded method.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class OverloadReference(WorkToyException, SyntaxError):
  """
  OverloadReference is raised when a reference through 'THIS', such as
  'THIS[Ruler].size', names an overloaded method. Such a reference stands
  for a descriptor as the subclass will hold it, a clone placed on the
  subclass as it is created, and for an overloaded name that clone was a
  copy of the dispatcher of the parent. It replaced the dispatcher the
  namespace of the subclass builds, so the subclass lost the overloads
  its body declared, and a body refused at a later line left the clone
  for the next subclass of the parent, which lost its overloads without a
  word. A subclass declares its own overloads of an inherited name with
  '@overload' in its body, and keeps the inherited ones. The refusal
  comes at the line of the reference, before anything is recorded. It
  subclasses 'SyntaxError', as the other refusals of a class-body line
  do.

  Attributes
  ----------
  parentName : str
    The name of the class named in the subscript.
  fieldName : str
    The overloaded name the reference reads.
  """

  __slots__ = ('parentName', 'fieldName')

  def __init__(self, parentName: str, fieldName: str) -> None:
    self.parentName = parentName
    self.fieldName = fieldName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The reference 'THIS[%s].%s' names an overloaded method. A
    reference through 'THIS' stands for a descriptor the subclass will
    hold, such as an 'AttriBox', and an overloaded method is none."""
    rule = """A subclass declares its own overloads of '%s' with
    '@overload' in its body, and keeps the overloads it inherits."""
    names = (self.parentName, self.fieldName)
    return textFmt(spec % names, rule % self.fieldName)

  __repr__ = __str__
