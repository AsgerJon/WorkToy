"""TestError is for testing."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


class TestError(Exception):
  """some testing!"""

  def __init__(self, who: str) -> None:
    self._who = who

  def _getWho(self) -> str:
    """Getter-function for the message"""
    return self._who

  def __repr__(self) -> str:
    """Code Representation"""
    return '%s(%s)' % (type(self), self._getWho())

  def __str__(self) -> str:
    """String Representation"""
    msg = """%s: They just caught me!, Shaggy: Say it wasn't you!"""
    return msg % self._getWho()
