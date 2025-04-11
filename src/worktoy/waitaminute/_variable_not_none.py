"""VariableNotNone should be raised when a variable is unexpectedly not
None."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class VariableNotNone(Exception):
  """VariableNotNone should be raised when a variable is unexpectedly not
  None."""

  __variable_name__ = None

  def __init__(self, variableName: str = None) -> None:
    """Initialize the VariableNotNone object."""
    if variableName is None:
      Exception.__init__(self, 'Expected variable to be None')
    else:
      self.__variable_name__ = variableName
      info = "Variable at name: '%s' is not None"
      Exception.__init__(self, info % variableName)
