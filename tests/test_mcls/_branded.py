"""
Branded is a worktoy class with a text and a hash of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject


class Branded(BaseObject):
  """
  A class may write itself and hash itself through '__class_str__',
  '__class_repr__' and '__class_hash__'. 'Branded' writes 'branded:'
  before its name, writes a call of its name as its repr, and hashes to
  forty-two.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CLASS HOOKS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_str__(cls) -> str:
    return 'branded:%s' % cls.__name__

  @classmethod
  def __class_repr__(cls) -> str:
    return '%s()' % cls.__name__

  @classmethod
  def __class_hash__(cls) -> int:
    return 42
