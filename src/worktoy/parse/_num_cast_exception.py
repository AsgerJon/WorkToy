"""NumCastException is a custom exception subclass of ValueError raised by
the 'numCast' function when unable to caste a value to a given type. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class NumCastException(TypeError):
  """NumCastException is a custom exception subclass of ValueError raised by
  the 'numCast' function when unable to caste a value to a given type. """

  def __init__(self, value: object, target: type) -> None:
    e = """Unable to cast object: '%s' to numeric type: '%s'!"""
    TypeError.__init__(self, e % (value, target))
