"""
RougeVertBleu example test.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.utilities import maybe

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Iterator


class RougeVertBleu(BaseObject):
  """
  Alternative to 'RGB' based on the more flexible 'BaseObject'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __registered_instances__ = None

  #  Fallback Variables

  #  Private Variables

  #  Public Variables

  #  Virtual Variables
  red = AttriBox[int](255)
  green = AttriBox[int](255)
  blue = AttriBox[int](255)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getRegisteredInstances(cls) -> tuple[Self, ...]:
    return maybe(cls.__registered_instances__, ())

  @classmethod
  def _registerInstance(cls, instance: Self) -> None:
    registered = cls._getRegisteredInstances()
    cls.__registered_instances__ = (*registered, instance)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[int]:
    yield self.red
    yield self.green
    yield self.blue

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int, int)
  def __init__(self, *args, ) -> None:
    self.red, self.green, self.blue = args

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.__init__(*other, )

  @overload(int)
  def __init__(self, monoChrome: int) -> None:
    self.__init__(monoChrome, monoChrome, monoChrome)

  @overload()
  def __init__(self, *args, ) -> None:
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
