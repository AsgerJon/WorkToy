"""
RepeatedFieldException is raised when an 'EZData' class is called with a
value for the same field both by position and by keyword.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class RepeatedFieldException(NoPickle, TypeError):
  """
  RepeatedFieldException is raised when an 'EZData' class is called with a
  value for the same field both by position and by keyword, as in
  'Point(1, x=2)'. One of the two values would otherwise replace the other
  without a word. It subclasses 'TypeError', as Python's own refusal of
  multiple values for one argument does.

  Attributes
  ----------
  cls : type
    The 'EZData' class that received the field twice.
  fieldName : str
    The name of the field given both by position and by keyword.
  """

  __slots__ = ('cls', 'fieldName')

  def __init__(self, cls: type, fieldName: str) -> None:
    self.cls = cls
    self.fieldName = fieldName
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData class '%s' received the field '%s' both by
    position and by keyword."""
    info = infoSpec % (self.cls.__name__, self.fieldName)
    return textFmt(info)

  __repr__ = __str__
