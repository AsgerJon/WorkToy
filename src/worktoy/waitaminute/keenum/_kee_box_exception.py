"""
KeeBoxException is raised when a 'KeeBox' fails to resolve to a member of
its enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class KeeBoxException(Exception):
  """
  KeeBoxException is a custom exception class raised to indicate that a
  'KeeBox' object failed to resolve to the underlying member.

  Attributes
  ----------
  box : KeeBox
    The 'KeeBox' descriptor that failed to resolve.
  posArgs : tuple
    The arguments that failed to resolve to a member.
  """

  __slots__ = ('box', 'posArgs')

  def __init__(self, box: Any, args: Any) -> None:
    self.box, self.posArgs = box, args
    Exception.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """KeeBox object: '%s' failed to resolve with arguments:
    <br><tab>%s<br>"""
    boxStr = str(self.box)
    argSpec = """<%s: %s>"""
    argTypes = (*(type(arg).__name__ for arg in self.posArgs),)
    argStrs = (*(repr(arg) for arg in self.posArgs),)
    argInfos = (*(argSpec % (t, s) for s, t in zip(argStrs, argTypes)),)
    argInfo = '<br><tab>'.join(argInfos)
    info = infoSpec % (boxStr, argInfo)
    from ...utilities import textFmt
    return textFmt(info, )

  __repr__ = __str__
