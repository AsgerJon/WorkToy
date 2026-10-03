"""
KeeCaseException is raised when the name of a 'KeeNum' member or a
'KeeFlags' flag is not upper case.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import NoPickle


class KeeCaseException(NoPickle, ValueError):
  """
  Raised when the name of a 'KeeNum' member or of a 'KeeFlags' flag is
  not upper case (the check is 'name.isupper()'); lowercase or mixed-case
  names are rejected. Lookups by call or subscript ignore case.

  Attributes
  ----------
  name : str
    The name that failed the upper-case check.
  """

  __slots__ = ('name',)

  def __init__(self, name: str, ) -> None:
    self.name = name
    ValueError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The members of an enumeration, and the flags of a
    'KeeFlags' class, must have upper case names, but received: '%s'"""
    from ...utilities import textFmt
    return textFmt(infoSpec % self.name)

  __repr__ = __str__
