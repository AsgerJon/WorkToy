"""
ClassKeywordError is raised when an 'EZData' class statement passes a class
keyword that no part of 'EZData' reads.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class ClassKeywordError(NoPickle, TypeError):
  """
  ClassKeywordError is raised at the class statement of an 'EZData' class
  that passes a class keyword which is none of the options 'EZData' reads,
  such as 'frozn=True' for 'frozen=True', when no base of the class has
  an '__init_subclass__' of its own that could take it. Such a keyword
  would otherwise be dropped without a word, leaving the class without
  the option it was meant to set. The message lists the accepted
  spellings. With such a base present the keyword goes down the
  '__init_subclass__' chain instead, where the base takes it or 'object'
  refuses it.

  Attributes
  ----------
  clsName : str
    The name of the 'EZData' class under construction.
  keyword : str
    The class keyword that no part of 'EZData' reads.
  accepted : tuple[str, ...]
    The class keywords the class statement accepts.
  """

  __slots__ = ('clsName', 'keyword', 'accepted')

  def __init__(self, clsName: str, keyword: str, *accepted: str) -> None:
    self.clsName = clsName
    self.keyword = keyword
    self.accepted = accepted
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData class '%s' received the class keyword '%s', which
    it does not accept. The accepted class keywords are: %s."""
    accepted = ', '.join("""'%s'""" % key for key in self.accepted)
    info = infoSpec % (self.clsName, self.keyword, accepted)
    return textFmt(info)

  __repr__ = __str__
