"""
OverloadConflict is raised when one class body binds a name both to
overloads and to a plain definition.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class OverloadConflict(NoPickle, SyntaxError):
  """
  OverloadConflict is raised when one class body binds a name both to
  overloads and to a plain definition, which is any binding that is not
  an 'overload': a function, a 'property', a 'staticmethod', a constant,
  or a value another namespace hook claims, such as an 'EZField'. Only
  one of the two could take the name, and which one says nothing about
  the order they were written in, so the class body fails at the second
  of them instead. A subclass may still replace what it inherits, an
  overloaded method with a plain one or the other way around. It
  subclasses 'SyntaxError', as the other refusals of a class-body line
  do.

  Attributes
  ----------
  className : str
    The name of the class under construction.
  overloadName : str
    The name bound both ways.
  overloadsFirst : bool
    Whether the overloads came before the plain definition.
  """

  __slots__ = ('className', 'overloadName', 'overloadsFirst',)

  def __init__(
      self,
      className: str,
      overloadName: str,
      overloadsFirst: bool,
  ) -> None:
    self.className = className
    self.overloadName = overloadName
    self.overloadsFirst = overloadsFirst
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    if self.overloadsFirst:
      spec = """The class body of '%s' overloads the name '%s' and then
      binds it to a plain definition."""
    else:
      spec = """The class body of '%s' binds the name '%s' to a plain
      definition and then overloads it."""
    rule = """One class body may give a name either overloads or a plain
    definition, not both."""
    info = spec % (self.className, self.overloadName)
    return textFmt(info, rule)

  __repr__ = __str__
