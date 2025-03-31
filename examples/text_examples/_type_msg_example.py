"""This example demonstrates how to use the typeMsg function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import wordWrap, typeMsg


def typeMsgExample() -> None:
  """This example demonstrates how to use the typeMsg function."""

  def foo(bar: int) -> None:
    if not isinstance(bar, int):
      e = typeMsg('bar', bar, int)
      raise TypeError(e)
    print(bar)

  susBar = 'sixty-nine'
  try:
    foo(susBar)  # That's not an int!
  except TypeError as typeError:
    errorMsg = str(typeError)  # Let's wrap this string at 50 characters
    wrapped = wordWrap(50, errorMsg)  # We apply 'str.join' to the list
    msg = '\n'.join(wrapped)
    print(msg)
