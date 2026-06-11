"""
KwargsOnlyException is raised when an EZData subclass declared with
'kw_only=True' receives positional arguments.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt


class KwargsOnlyException(TypeError):
  """
  Raised when an EZData subclass declared with 'kw_only=True' is
  called with positional arguments. Such a subclass accepts only
  keyword arguments at construction.
  """

  __slots__ = ('cls', 'argCount')

  def __init__(self, *args) -> None:
    cls, nArgs, *_ = [*args, None, None]
    self.cls = cls
    self.argCount = nArgs
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData subclass '%s' was declared with 'kw_only=True'
    but received %d positional arguments. """
    info = infoSpec % (self.cls.__name__, self.argCount)
    return textFmt(info, )

  __repr__ = __str__
