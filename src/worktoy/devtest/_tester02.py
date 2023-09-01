"""CUNTS"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from worktoy.waitaminute import DisabledFunctionError, TypeSupportError
from worktoy.waitaminute._argument_error import ArgumentError


class FUCK:
  """YOU"""

  def __init__(self, cunt: int) -> None:
    if not isinstance(cunt, int):
      expType = int
      actVal = cunt
      argName = 'cunt'
      raise TypeSupportError(expType, actVal, argName)

  def shit(self) -> None:
    print('fuck you')


class YOU(FUCK):
  """KILL"""

  def shit(self) -> Never:
    """Yourself"""

    raise DisabledFunctionError(FUCK, YOU)
