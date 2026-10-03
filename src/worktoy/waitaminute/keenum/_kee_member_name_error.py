"""
KeeMemberNameError is raised when a 'KeeFlags' class body binds a name
that one of its members takes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class KeeMemberNameError(NoPickle, SyntaxError):
  """
  KeeMemberNameError is raised as a 'KeeFlags' class is created when its
  class body binds a name that one of its members takes: 'NULL', or the
  names of some of its flags joined by '_' in the order they were
  declared, as in 'READ_WRITE = 'rw'' beside the flags 'READ' and
  'WRITE'. The member would replace the attribute without a word. It is
  raised as the class is created, since the flags that make up the name
  may be declared after the attribute. It subclasses 'SyntaxError', as
  the other refusals of a class-body line do.

  Attributes
  ----------
  clsName : str
    The name of the 'KeeFlags' class under construction.
  memberName : str
    The name the class body binds, which a member takes.
  """

  __slots__ = ('clsName', 'memberName',)

  def __init__(self, clsName: str, memberName: str) -> None:
    self.clsName = clsName
    self.memberName = memberName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    infoSpec = """The class body of KeeFlags class '%s' binds '%s', but a
    member of the class takes that name."""
    info = infoSpec % (self.clsName, self.memberName)
    return textFmt(info)

  __repr__ = __str__
