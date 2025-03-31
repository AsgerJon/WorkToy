"""NameMismatchException is a subclass of ValueError and indicates that a
Dispatch object received overloaded functions with different names. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace


class NameMismatchException(ValueError):
  """NameMismatchException is a subclass of ValueError and indicates that a
  Dispatch object received overloaded functions with different names. """

  def __init__(self, oldName: str, newName: str) -> None:
    e = """The function '%s' was already registered with the name '%s'!"""
    ValueError.__init__(self, monoSpace(e % (newName, oldName)))
