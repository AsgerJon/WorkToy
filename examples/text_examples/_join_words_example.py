"""This example demonstrates how to use the joinWords function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import joinWords


def joinWordsExample() -> None:
  """This example demonstrates how to use the joinWords function."""
  foo = ['Tom', 'Dick', 'Harry']
  print(joinWords(foo[0]))  # 'Tom'
  print(joinWords(*foo[:2]))  # 'Tom and Dick'
  print(joinWords(*foo[:3]))  # 'Tom, Dick and Harry'
