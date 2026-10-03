"""
KwargsOnlyException is raised when an EZData subclass declared with
'kwOnly=True' receives positional arguments.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class KwargsOnlyException(NoPickle, TypeError):
  """
  Raised when an EZData subclass declared with 'kwOnly=True' (or a
  synonym such as 'keywordOnly' or 'kw_only') is called with positional
  arguments. Such a subclass accepts only keyword arguments at
  construction.
  """

  __slots__ = ('cls', 'argCount')

  def __init__(self, *args) -> None:
    cls, nArgs, *_ = [*args, None, None]
    self.cls = cls
    self.argCount = nArgs
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData subclass '%s' was declared with 'kwOnly=True'
    but received %d positional %s. """
    arguments = 'argument' if self.argCount == 1 else 'arguments'
    info = infoSpec % (self.cls.__name__, self.argCount, arguments)
    return textFmt(info, )

  __repr__ = __str__
