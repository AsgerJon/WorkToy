"""
UnpackException is raised when 'unpack' finds no iterable argument in
strict mode.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class UnpackException(ValueError):
  """
  UnpackException is raised when an unpacking operation finds no argument
  requiring unpacking. It is raised by the 'unpack' function in the
  'worktoy.utilities' package when strict mode is enabled (the default) and
  no iterable is found among the arguments. 'unpack' does not treat 'str'
  or 'bytes' as unpackable iterables.

  Attributes
  ----------
  posArgs : tuple
    The positional arguments 'unpack' received, none of which was an
    unpackable iterable.
  """

  __slots__ = ('posArgs',)

  def __init__(self, *args) -> None:
    self.posArgs = args
    ValueError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """'unpack' found no iterable argument from: \n'%s'\nand is 
    running in strict mode (default). Change this by setting keyword 
    argument 'strict' to False."""
    argStr = '\n  '.join([str(arg) for arg in self.posArgs])
    info = infoSpec % argStr
    return textFmt(info)

  __repr__ = __str__
