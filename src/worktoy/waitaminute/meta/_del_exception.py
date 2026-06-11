"""
DelException is raised when a class body defines '__del__' without the
'trustMeBro=True' keyword.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt


class DelException(SyntaxError):
  """
  DelException is raised when a class body defines '__del__' without the
  'trustMeBro=True' class keyword. A stray '__del__' is almost always a
  typo for '__delete__'; pass 'trustMeBro=True' to keep a genuine one. It
  subclasses 'SyntaxError'.

  Attributes
  ----------
  mcls : type
    The metaclass building the class.
  name : str
    The name of the class under construction.
  bases : tuple[type, ...]
    The base classes of the class under construction.
  space : object
    The namespace in which '__del__' was found.
  """
  __slots__ = ('mcls', 'name', 'bases', 'space')

  def __init__(self, *args) -> None:
    self.mcls, self.name, self.bases, self.space = args
    SyntaxError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """When attempting to derive a class named '%s' from the 
    metaclass '%s', the '__del__' method was found in the namespace! This 
    is almost always a typo, but if not this error can be suppressed by 
    passing the keyword argument 'trustMeBro=True' during class creation. """
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(self.bases, tuple)
    if self.bases:
      mclsSpec = """%s with bases: (%s)"""
    else:
      mclsSpec = """%s%s"""
    basesStr = ', '.join(base.__name__ for base in self.bases)
    mclsName = mclsSpec % (self.mcls.__name__, basesStr)
    info = infoSpec % (self.name, mclsName)
    return textFmt(info, )

  __repr__ = __str__
