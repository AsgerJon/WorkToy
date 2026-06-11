"""
KeeCaseException is raised when a 'KeeNum' member name is not upper-case.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations


class KeeCaseException(ValueError):
  """
  Raised when a 'KeeNum' member name is not upper-case (the check is
  'name.isupper()'); lowercase or mixed-case names are rejected.

  Attributes
  ----------
  name : str
    The member name that failed the upper-case check.
  """

  __slots__ = ('name',)

  def __init__(self, name: str, ) -> None:
    self.name = name
    ValueError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """KeeNum members must have upper case names, but received: 
    '%s'"""
    from ...utilities import textFmt
    return textFmt(infoSpec % self.name)

  __repr__ = __str__
