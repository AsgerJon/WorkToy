"""
Tests how well KeeNum classes resolve their members.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import auto, KeeNum
from worktoy.parse import maybe
from worktoy.waitaminute import TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class Integer:
  """
  Integer wrapper for integer values not used for indexing.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_value__ = 0

  #  Private Variables
  __inner_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValue(self) -> int:
    """
    Returns the inner value.
    """
    return maybe(self.__inner_value__, self.__fallback_value__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setValue(self, value: int) -> None:
    """
    Sets the inner value.
    """
    if not isinstance(value, int):
      raise TypeException('value', value, int)
    self.__inner_value__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, value: int) -> None:
    """
    Initializes the Integer wrapper with a value.
    """
    try:
      self._setValue(int(value))
    except Exception as exception:
      raise TypeException('value', value, int) from exception

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __int__(self, ) -> int:
    """
    Returns the inner value as an integer.
    """
    return self._getValue()

  def __getattr__(self, key: str) -> Any:
    """
    If key is the name of a method in 'int', return wrapper simulating
    bound method.
    """
    try:
      intFunc = getattr(int, key)
    except AttributeError as attributeError:
      raise attributeError
    else:
      selfValue = self._getValue()

      def wrapper(other: int) -> int:
        """
        Simulates a bound method of 'int'.
        """
        return intFunc(selfValue, other)

      return wrapper

  def __eq__(self, other: Any) -> bool:
    """
    Compares the inner value with another value.
    """
    if isinstance(other, Integer):
      return True if self._getValue() == other._getValue() else False
    if isinstance(other, int):
      return True if self._getValue() == other else False
    return False


class Speed(KeeNum):
  """
  Speed wrapper for integer values used for indexing.
  """
  FAST = auto(Integer(1))
  SLOW = auto(Integer(2))


# Test enum class
class Mode(KeeNum):
  FAST_MODE = auto('fast')
  SLOW_MODE = auto('slow')
  TURBO = auto('fast')  # duplicate value


class TestKeeNumLookup(TestCase):
  def test_nameLookupFlexible(self) -> None:
    self.assertIsInstance(Mode['FAST_MODE'], Mode)
    self.assertIs(Mode['fast_mode'], Mode.FAST_MODE)

  def test_indexLookup(self) -> None:
    self.assertIs(Mode[0], Mode.FAST_MODE)
    self.assertIs(Mode[1], Mode.SLOW_MODE)
    self.assertIs(Mode[2], Mode.TURBO)
    self.assertIs(Mode[-3], Mode.FAST_MODE)
    self.assertIs(Mode[-2], Mode.SLOW_MODE)
    self.assertIs(Mode[-1], Mode.TURBO)

  def test_valueLookup(self) -> None:
    self.assertIn(Mode['fast'], (Mode.FAST_MODE, Mode.TURBO))
    self.assertIs(Mode['slow'], Mode.SLOW_MODE)
