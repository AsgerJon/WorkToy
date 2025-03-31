"""This example demonstrates how to use the monoSpace function. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace


def monoSpaceExample() -> None:
  """This example demonstrates how to use the monoSpace function. """
  foo = """Welcome to the monoSpace documentation! <br> After that 
  convenient linebreak, we are done!"""
  bar = monoSpace(foo)
  print(bar)
