"""IllegalName is a custom exception raised to indicate that a namespace
entry is of a disallowed name. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..text import joinWords
from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Never


class IllegalName(Exception):
  """IllegalName is a custom exception raised to indicate that a namespace
  entry is of a disallowed name. """

  name = _Attribute()
  disallowedNames = _Attribute()

  def __init__(self, name: str, *disallowedNames) -> None:
    self.name = name
    self.disallowedNames = [*disallowedNames, ]
    if self.disallowedNames:
      infoSpec = """Tried setting name: '%s' which is on the list of 
      disallowed names: %s"""
      disallowedStr = joinWords(*self.disallowedNames, )
      info = infoSpec % (name, disallowedStr)
    else:
      infoSpec = """Tried setting disallowed name: '%s'!"""
      info = infoSpec % name
    Exception.__init__(self, info)
