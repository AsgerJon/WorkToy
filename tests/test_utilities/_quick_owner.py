"""
QuickOwner is a class exposing a private slot through 'QuickDesc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import QuickDesc


class QuickOwner:
  """
  The tests of 'QuickDesc' need an owner holding a private slot behind a
  public name, and one whose '__getattr__' answers for any missing
  attribute, so that a read of a slot never set is seen to ask it for
  the public name and never for the private key. 'QuickOwner' is both:
  'value' reads '__value__', 'missing' reads a slot no instance holds,
  and '__getattr__' answers with the name it was asked for.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __value__: int = 42

  #  Public Variables
  value = QuickDesc('__value__')
  missing = QuickDesc('__missing__')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getattr__(self, key: str) -> str:
    return key
