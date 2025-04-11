"""MissingVariable exception should be raised when a variable is missing
and requires initialization. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class MissingVariable(Exception):
  """MissingVariable exception should be raised when a variable is missing
  and requires initialization. """

  __variable_name__ = None
  __variable_type__ = None

  def __init__(self, variableName: str, variableType: type) -> None:
    """Initialize the MissingVariable object."""
    self.__variable_name__ = variableName
    self.__variable_type__ = variableType
    info = "Missing variable '%s' of type '%s'"
    Exception.__init__(self, info % (variableName, variableType))
