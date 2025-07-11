"""
TestWildcard tests the wildcard overloading functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import WILDCARD
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.static import overload
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class WildClass(BaseObject):
  """WildClass has an overloaded init method with overloads that use the
  WILDCARD sentinel."""

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)
  note = AttriBox[str]('')

  @overload(float, float, str)
  def __init__(self, x: float, y: float, note: str) -> None:
    """Initialize with two floats and a string."""
    self.x = x
    self.y = y
    self.note = note

  @overload(complex, str)
  def __init__(self, z: complex, note: str) -> None:
    self.__init__(z.real, z.imag, note)

  @overload(int, int, str)
  def __init__(self, x: int, y: int, note: str) -> None:
    """Initialize with two integers and a string."""
    self.__init__(float(x), float(y), note)

  @overload(float, float, WILDCARD)
  def __init__(self, x: float, y: float, note: Any) -> None:
    self.__init__(x, y, str(note))

  @overload(WILDCARD, WILDCARD, WILDCARD)
  def __init__(self, *args) -> None:
    """Initialize with WILDCARD for all arguments."""
    self.__init__(69.0, 420.0, 'all ur base are belong to us')


class TestWildcard(OverloadTest):
  """TestWildcard tests the wildcard overloading functionality."""

  def test_chill_init(self) -> None:
    """Testing 'normal' initialization."""
    wild1 = WildClass(3.14, 2.71, 'pi and e')
    self.assertEqual(wild1.x, 3.14)
    self.assertEqual(wild1.y, 2.71)
    self.assertEqual(wild1.note, 'pi and e')

    wild2 = WildClass(complex(1.0, 2.0), 'complex number')
    self.assertEqual(wild2.x, 1.0)
    self.assertEqual(wild2.y, 2.0)
    self.assertEqual(wild2.note, 'complex number')

    wild3 = WildClass(1, 2, 'integers')
    self.assertEqual(wild3.x, 1.0)
    self.assertEqual(wild3.y, 2.0)
    self.assertEqual(wild3.note, 'integers')

  def test_wild_init(self, ) -> None:
    """Testing initialization with WILDCARD."""
    callMeMaybe = lambda: None
    wild4 = WildClass(3.14, 2.71, callMeMaybe)
    self.assertEqual(wild4.x, 3.14)
    self.assertEqual(wild4.y, 2.71)
    self.assertEqual(wild4.note, str(callMeMaybe))

    wild5 = WildClass(1.0, 2.0, str)
    self.assertEqual(wild5.x, 1.0)
    self.assertEqual(wild5.y, 2.0)
    self.assertEqual(wild5.note, str(str))

    wild6 = WildClass(1, 2, WildClass)
    self.assertEqual(wild6.x, 1.0)
    self.assertEqual(wild6.y, 2.0)
    self.assertEqual(wild6.note, str(WildClass))

    wild7 = WildClass(69, 420, WILDCARD)
    self.assertEqual(wild7.x, 69.0)
    self.assertEqual(wild7.y, 420.0)
    self.assertEqual(wild7.note, str(WILDCARD))

  def test_crazy_town(self) -> None:
    """Testing the wildcard overload that takes WILDCARD for all
    arguments."""

    wild9 = WildClass(object, object, object, )
    self.assertEqual(wild9.x, 69.0)
    self.assertEqual(wild9.y, 420.0)
    self.assertEqual(wild9.note, 'all ur base are belong to us')
