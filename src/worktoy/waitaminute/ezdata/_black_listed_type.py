"""
BlackListedType is a custom exception raised when a blacklisted type is
encountered in the class body of an EZData class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class BlackListedType(WorkToyException, TypeError):
  """
  BlackListedType is raised when a blacklisted type is encountered in the
  class body of an EZData class.
  """

  clsName: str
  key: str
  value: Any

  __slots__ = ('clsName', 'key', 'value')

  def __init__(self, name: str, key: str, value: Any) -> None:
    self.clsName = name
    self.key = key
    self.value = value
    TypeError.__init__(self, name, key, value)

  def __str__(self) -> str:
    infoSpec = """Encountered blacklisted type '%s' in the class body of 
    '%s' for the name '%s'."""
    blackListed: str = type(self.value).__name__
    info: str = infoSpec % (blackListed, self.clsName, self.key)
    return textFmt(info)

  __repr__ = __str__
