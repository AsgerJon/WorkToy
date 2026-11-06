"""
Label is a worktoy class whose constructor takes its arguments in any
order, a copy of another label, or nothing.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Label(BaseObject):
  """
  The end-to-end tests of 'overload' need a class whose constructor is
  declared flexibly, with 'THIS' and bare. 'Label' holds a text and a
  count, taken in either order, copied from another label with a mark
  appended, or left at their defaults.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  text = AttriBox[str]('')
  count = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload.flex(str, int)
  def __init__(self, text: str, count: int) -> None:
    self.text = text
    self.count = count

  @overload(THIS)
  def __init__(self, other: Label) -> None:
    self.text = other.text + '!'
    self.count = other.count

  @overload()
  def __init__(self) -> None:
    pass
