"""
KeeMemberNameError is raised when an enumeration class body binds a name
that one of its members takes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class KeeMemberNameError(WorkToyException, SyntaxError):
  """
  KeeMemberNameError is raised when an enumeration class body binds a
  name that one of its members takes, and the member would replace the
  attribute without a word.

  For a 'KeeFlags' class the name is 'NULL', or the names of some of its
  flags joined by '_' in the order they were declared, as in
  'READ_WRITE = 'rw'' beside the flags 'READ' and 'WRITE'. It is raised
  as the class is created, since the flags that make up the name may be
  declared after the attribute.

  For a 'KeeNum' class the name is that of a 'Kee' declared in the body
  or inherited, bound to a plain value before or after the member, as in
  'RED = 'plain'' beside 'RED = Kee[int](1)'. It is raised at the second
  binding, in the class body.

  It subclasses 'SyntaxError', as the other refusals of a class-body
  line do.

  Attributes
  ----------
  clsName : str
    The name of the enumeration class under construction.
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
    infoSpec = """The class body of enumeration class '%s' binds '%s',
    but a member of the class takes that name."""
    info = infoSpec % (self.clsName, self.memberName)
    return textFmt(info)

  __repr__ = __str__
