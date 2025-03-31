"""This example demonstrates how to use the stringList function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import stringList


def stringListExample() -> None:
  """This example demonstrates how to use the stringList function."""
  foo = ['so', 'many', 'quotation', 'marks!']
  bar = stringList("""so, many, quotation, marks!""")
  print(foo == bar)  # True
