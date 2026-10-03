"""
ClaimedName is raised when a class body deletes a name that a namespace
hook claimed.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class ClaimedName(NoPickle, SyntaxError):
  """
  ClaimedName is raised when a class body deletes a name whose latest
  binding a namespace hook claimed, such as an 'overload', an 'EZField'
  or a 'Kee'. The hook took the value away from the namespace when the
  class body bound it, and registered it at once, so deleting the name
  could not undo the registration: the class would still be built with
  the value the class body meant to remove. A name bound to an ordinary
  value is deleted as in a plain class. It subclasses 'SyntaxError', as
  the other refusals of a class-body line do.

  It is raised as the class is created rather than at the deletion
  itself, since the interpreter replaces any exception a deletion in a
  class body raises with its own 'NameError', saying that the name is
  not defined.

  Attributes
  ----------
  className : str
    The name of the class under construction.
  keyName : str
    The name the class body deleted.
  """

  __slots__ = ('className', 'keyName',)

  def __init__(self, className: str, keyName: str) -> None:
    self.className = className
    self.keyName = keyName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class body of '%s' deletes '%s', which a namespace hook
    claimed when the class body bound it. The hook registered the value
    at once, so the name cannot be deleted."""
    info = spec % (self.className, self.keyName)
    return textFmt(info)

  __repr__ = __str__
