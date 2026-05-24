"""VariableNotNone should be raised when a variable is unexpectedly not
None."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class VariableNotNone(Exception):
  """VariableNotNone is raised when a variable expected to still be 'None'
  already holds a value. It guards write-once initialisation: a slot that
  must be assigned exactly once raises this exception on the second
  assignment.

  Attributes
  ----------
  name : str
    The name of the variable that was unexpectedly not 'None'.
  value : Any
    The existing value found at that name.
  """

  __slots__ = ('name', 'value')

  def __init__(self, *args) -> None:
    self.name, self.value, *_ = [*args, None, None]
    Exception.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """Unexpected value: '%s' at name '%s' expected to be 
    None!"""
    valueStr = textFmt(str(self.value), )
    name = self.name
    return textFmt(infoSpec % (valueStr, name), )

  __repr__ = __str__
