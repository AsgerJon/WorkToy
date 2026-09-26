"""
KeeFlagNameError is raised when a 'KeeFlags' class body declares a flag
whose name contains an underscore.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt


class KeeFlagNameError(ValueError):
  """
  KeeFlagNameError is raised at class construction time when a
  'KeeFlags' class body declares a flag whose name contains an
  underscore. The name of a combined member joins the names of its flags
  with underscores, as in 'READ_WRITE', so an underscore inside a flag
  name makes names ambiguous: with the flags 'READ', 'ONLY' and
  'READ_ONLY', two members would both be named 'READ_ONLY'. Refusing
  such names keeps every member name, and every lookup by name, exact.

  Attributes
  ----------
  clsName : str
    The name of the 'KeeFlags' class under construction.
  name : str
    The flag name that contains an underscore.
  """

  __slots__ = ('clsName', 'name')

  def __init__(self, clsName: str, name: str) -> None:
    self.clsName = clsName
    self.name = name
    ValueError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """KeeFlags class '%s' declares the flag '%s', but flag
    names may not contain '_', since it joins the flag names in the name
    of a combined member, as in 'READ_WRITE'."""
    info = infoSpec % (self.clsName, self.name)
    return textFmt(info)

  __repr__ = __str__
