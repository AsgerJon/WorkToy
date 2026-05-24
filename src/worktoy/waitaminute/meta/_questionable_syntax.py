"""QuestionableSyntax is raised when a name is encountered that is likely
a typo, such as '__set_item__' instead of '__setitem__' or '__setname__'
instead of '__set_name__'. It subclasses 'SyntaxError' and is used to
flag code that is likely incorrect even though Python itself would
accept it."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class QuestionableSyntax(SyntaxError):
  """
  QuestionableSyntax is raised when a class body defines a name that is a
  near-miss for a real dunder, such as '__set_item__' for '__setitem__' or
  '__setname__' for '__set_name__'. Python would silently accept the typo
  as an ordinary attribute, so this exception flags it loudly instead. It
  subclasses 'SyntaxError'.

  Attributes
  ----------
  realName : str
    The correctly spelled dunder the name was probably meant to be.
  derpName : str
    The misspelled name that was actually used.
  """

  __slots__ = ('derpName', 'realName',)

  def __init__(self, realName: str, derpName: str, ) -> None:
    self.derpName = derpName
    self.realName = realName
    SyntaxError.__init__(self, )

  def __str__(self) -> str:
    spec = """Received name '%s' which is similar enough to '%s' to be
    a likely typo."""
    info = spec % (self.derpName, self.realName)
    return textFmt(info)

  __repr__ = __str__
