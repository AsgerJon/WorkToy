"""The 'typecastExample' function demonstrates how to use the 'typeCast'
function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import typeCast
from worktoy.text import typeMsg


def typeCastExample() -> None:
  """The 'typecastExample' function demonstrates how to use the 'typeCast'
  function."""

  def intSquare(base: int) -> int:
    """Return the square of the given integer. The input is typecast to an
    integer."""
    intBase = typeCast(base, int) ** 2
    if isinstance(intBase, int):
      return intBase * intBase
    e = typeMsg('intBase', intBase, int)
    raise TypeError(e)

  testValues = [69, 420.0, '1337', 80085. + 0j, 'lmao']
  for value in testValues:
    try:
      res = intSquare(value)
      print("""Squaring: '%s' -> '%s'""" % (value, res))
    except TypeError as exception:
      print("""Trying to square: '%s' lead to: '%s'""" % (value, exception))
