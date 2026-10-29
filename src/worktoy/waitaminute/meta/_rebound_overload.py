"""
ReboundOverload is raised when one class body binds the same 'overload'
object a second time.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class ReboundOverload(WorkToyException, SyntaxError):
  """
  ReboundOverload is raised when one class body binds the same 'overload'
  object a second time, under another name, as in '__radd__ = __add__',
  or under the same one. The second name would receive a copy of the
  overloads of the first, but the copy counts those the class inherits
  as its own, so the two names could call different functions for one
  call: in a subclass declaring '@overload(complex)' beside an inherited
  '@overload(float)', 'z + 1' would reach the inherited function and
  '1 + z' the subclass's. The class body fails at the second binding
  instead. The second name takes a method of its own, which may call the
  first. Another class body may bind the same 'overload' object again. It
  subclasses 'SyntaxError', as the other refusals of a class-body line
  do.

  Attributes
  ----------
  className : str
    The name of the class under construction.
  firstName : str
    The name the class body bound the 'overload' object to first.
  newName : str
    The name of the second binding.
  """

  __slots__ = ('className', 'firstName', 'newName',)

  def __init__(self, className: str, firstName: str, newName: str) -> None:
    self.className = className
    self.firstName = firstName
    self.newName = newName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class body of '%s' binds the overload of '%s' a second
    time, at '%s'. An overload is bound once per class body; give '%s' a
    method of its own, which may call '%s'."""
    names = (
      self.className, self.firstName, self.newName, self.newName,
      self.firstName,
    )
    return textFmt(spec % names)

  __repr__ = __str__
