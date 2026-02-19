"""
Pen encapsulates a color and a width for the purpose of testing the KeeBox
class. Rather than having the color as an 'AttriBox' with 'valueType' of
'RGB', 'Pen' owns a 'KeeBox' instance with 'valueType' of 'ColorNum'. The
'width' uses 'AttriBox'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle, randint
from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.keenum import KeeBox
from worktoy.mcls import BaseObject
from . import ColorNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any, Iterator


class Pen(BaseObject):
  """
  Pen encapsulates a color and a width for the purpose of testing the KeeBox
  class. Rather than having the color as an 'AttriBox' with 'valueType' of
  'RGB', 'Pen' owns a 'KeeBox' instance with 'valueType' of 'ColorNum'. The
  'width' uses 'AttriBox'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables

  #  Public Variables
  color = KeeBox[ColorNum]('YELLOW')
  width = AttriBox[int](1)

  @overload(ColorNum, int)
  def __init__(self, color: ColorNum, width: int) -> None:
    self.color = color
    self.width = width

  @overload(ColorNum, )
  def __init__(self, color: ColorNum) -> None:
    self.color = color

  @overload(int, )
  def __init__(self, width: int) -> None:
    self.width = width

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.color = other.color
    self.width = other.width

  @overload()
  def __init__(self, ) -> None:
    pass

  @classmethod
  def rand(cls, ) -> Self:
    colorIndex = randint(0, len(cls.color.fieldType) - 1)
    width = randint(1, 4)
    color = [m for m in cls.color.fieldType][colorIndex]
    return cls(color, width)

  @classmethod
  def rands(cls, n: int = None) -> tuple[Self, ...]:
    if n is None:
      return (cls.rand(),)
    return (*(cls.rand() for _ in range(n)),)

  @classmethod
  def fullSample(cls) -> Iterator[Self]:
    for member in cls.color.fieldType:
      for width in range(1, 5):
        yield cls(member, width)
