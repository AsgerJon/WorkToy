"""
RedundantKeyword warns that a function received a keyword it does not
read, and went on without it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import WorkToyWarning

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class RedundantKeyword(WorkToyWarning, UserWarning):
  """
  Python does not refuse an unknown keyword given to a function that
  collects its options in '**kwargs': the function reads the names it
  knows and the rest is dropped. A misspelled option is therefore never
  read, the function runs on its default, and the caller is not told.
  RedundantKeyword is given in that case: the call is carried out as it
  would be without the keyword, and the warning names the function, the
  keyword it does not read, and the keywords it does.

    RedundantKeyword(joinWords, 'seperator', 'sep').warn()

  It is offered to the projects built upon 'worktoy' as much as to
  'worktoy' itself: a project subclasses it in a package of its own,
  as the 'WorkToyWarning' docstring describes.

  Attributes
  ----------
  receiver : Any
    The function that received the keyword, or its name.
  keyword : str
    The keyword the function does not read.
  options : tuple of str
    The keywords the function does read, which may be none.
  """

  __slots__ = ('receiver', 'keyword', 'options')

  def __init__(self, receiver: Any, keyword: str, *options) -> None:
    UserWarning.__init__(self, )
    self.receiver = receiver
    self.keyword = keyword
    self.options = options

  def __str__(self) -> str:
    infoSpec = """'%s' received the keyword '%s', which it does not read,
    and went on without it! %s"""
    if self.options:
      quoted = ["""'%s'""" % option for option in self.options]
      reads = """It reads: %s.""" % str.join(', ', quoted)
    else:
      reads = """It reads no keyword."""
    name = self._nameOf(self.receiver)
    info = infoSpec % (name, self.keyword, reads)
    return textFmt(info)

  __repr__ = __str__
