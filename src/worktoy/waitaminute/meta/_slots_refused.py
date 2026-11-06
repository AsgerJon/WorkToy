"""
SlotsRefused is raised when the body of a class built by a worktoy
metaclass binds '__slots__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class SlotsRefused(WorkToyException, SyntaxError):
  """
  SlotsRefused is raised when the body of a class built by a metaclass
  based on 'AbstractMetaclass', as every 'BaseObject' class is, binds
  '__slots__'. A class declares '__slots__' to do without an instance
  dict, saving memory, or to refuse attributes nobody declared. An
  instance of a worktoy class always has a dict, since 'Object' and the
  boxes keep their state there, so '__slots__' could do neither: it used
  to be accepted, and the instances went on taking any attribute. The
  class body fails at the line binding it instead, and so does a class
  rebuilt with '__slots__' from the dictionary of another, as
  'dataclass(slots=True)' rebuilds a class. Slots a base declares outside
  worktoy are no concern of the class body. It subclasses 'SyntaxError',
  as the other refusals of a class-body line do.

  Attributes
  ----------
  className : str
    The name of the class whose body binds '__slots__'.
  """

  __slots__ = ('className',)

  def __init__(self, className: str) -> None:
    self.className = className
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class body of '%s' binds '__slots__'. An instance of a
    worktoy class always has a '__dict__', where 'Object' and the boxes
    keep their state, so '__slots__' can neither do without the dict nor
    refuse attributes nobody declared."""
    rule = """Declare the attributes with 'AttriBox' or 'Field'; a class
    that needs '__slots__' is written as a plain class."""
    return textFmt(spec % self.className, rule)

  __repr__ = __str__
