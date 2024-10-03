"""IllegalAttributeException should be raised when a FastObject subclass
tries to define a non-AttriBox attribute."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace


class IllegalAttributeException(Exception):
  """IllegalAttributeException should be raised when a FastObject subclass
  tries to define a non-AttriBox attribute."""

  def __init__(self, key: str, value: object) -> None:
    """The arguments provided should be the key to at which the attribute
    occurs and value should be the value of the attribute."""
    cls = type(value)
    name = cls.__name__
    e = """Attributes are required to be instances of AttriBox, 
    but received '%s' of type '%s' at key: '%s'!""" % (value, name, key)
    Exception.__init__(self, monoSpace(e))
