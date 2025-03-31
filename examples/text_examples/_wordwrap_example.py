"""This example demonstrates how to use the wordWrap function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import wordWrap


def wordWrapExample() -> None:
  """This example demonstrates how to use the wordWrap function."""
  foo = """This is a long string that needs to be wrapped. It is 
  important that the wrapping is done correctly. Otherwise, the text 
  will not be readable. """
  lineWidth: int = 40  # The line must not exceed 40 characters
  bar: list[str] = wordWrap(lineWidth, foo)  # Returns a list
  for line in bar:
    print(line)
