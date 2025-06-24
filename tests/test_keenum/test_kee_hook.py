"""
TestKeeHook confirms the functionality provided by the KeeHook class by
creating new derived classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.text import stringList
from worktoy.waitaminute import TypeException, KeeNumTypeException, \
  DuplicateKeeNum, EmptyKeeNumError, IllegalInstantiation
from worktoy.keenum import KeeHook, KeeNum
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestKeeHook(TestCase):
  """TestKeeHook confirms the functionality provided by the KeeHook class by
  creating new derived classes."""

  def test_good_keenum(self) -> None:
    """
    Test of a good KeeNum enumeration
    """

    class RomanNumeral(KeeNum):
      """RomanNumeral is a KeeNum enumeration for Roman numerals."""
      I = (1,)
      II = (2,)
      III = (3,)
      IV = (4,)
      V = (5,)
      VI = (6,)
      VII = (7,)
      VIII = (8,)
      IX = (9,)
      X = (10,)
      L = (50,)
      C = (100,)
      D = (500,)
      M = (1000,)

      def callMeMaybe(self) -> None:
        """
        Gotta get that coverage!
        """

    expectedValues = [*range(1, 11), 50, 100, 500, 1000]
    for num, exp in zip(RomanNumeral, expectedValues):
      self.assertEqual(num.value, (exp,))

    numNames = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
                'L', 'C', 'D', 'M']
    for name, value in zip(numNames, expectedValues):
      self.assertEqual(RomanNumeral[name].value, (value,))
      self.assertEqual(RomanNumeral[name].name, name)

    for i, member in enumerate(RomanNumeral):
      self.assertIs(RomanNumeral[member.name], member)
      self.assertIs(RomanNumeral[i], member)
      self.assertIs(RomanNumeral(member.name), member)
      self.assertIs(RomanNumeral(i), member)

  def test_bad_keenum(self) -> None:
    """
    Test of a KeeNum enumeration with a bad value
    """

    with self.assertRaises(KeeNumTypeException) as context:
      class BrehNum(KeeNum):
        """BrehNum is a KeeNum enumeration with a bad value."""
        ONE = 1
        TWO = '2'
    e = context.exception
    self.assertEqual(e.memberName, 'TWO')
    self.assertEqual(e.memberValue, '2')
    self.assertEqual(e.expectedType, int)

  def test_duplicate_keenum(self) -> None:
    """
    Test of a KeeNum enumeration with a duplicate value
    """

    with self.assertRaises(DuplicateKeeNum) as context:
      class DuplicateNum(KeeNum):
        """DuplicateNum is a KeeNum enumeration with a duplicate value."""
        ONE = 1
        TWO = 2
        ONE = 69
    e = context.exception
    self.assertEqual(e.memberName, 'ONE')
    self.assertEqual(e.memberValue, 69)

  def test_empty_keenum(self) -> None:
    """
    Test of an empty KeeNum enumeration
    """

    with self.assertRaises(EmptyKeeNumError) as context:
      class EmptyNum(KeeNum):
        """EmptyNum is a KeeNum enumeration with no members."""
        pass
    e = context.exception
    self.assertEqual(e.className, 'EmptyNum')

  def test_bad_resolution(self) -> None:
    """
    Test of a KeeNum enumeration with a bad resolution
    """

    class CountingWithAsger(KeeNum):
      ONE = 1
      TWO = 2

    with self.assertRaises(IllegalInstantiation) as context:
      _ = CountingWithAsger(69)
    e = context.exception
    self.assertIs(e.cls, CountingWithAsger)

  def test_indexed_enumerations(self, ) -> None:
    """
    Test of indexed enumerations
    """

    class WeekDay(KeeNum):
      """WeekDay is a KeeNum enumeration for weekdays."""

      MONDAY = 'montag'
      TUESDAY = 'dienstag'
      WEDNESDAY = 'mittwoch'
      THURSDAY = 'donnerstag'
      FRIDAY = 'freitag'
      SATURDAY = 'samstag'
      SUNDAY = 'sonntag'

    for i, day in enumerate(WeekDay):
      self.assertIs(WeekDay[i], day)
      self.assertIs(WeekDay(i), day)

  def test_value_typed_kee_num(self) -> None:
    """
    Test of a KeeNum enumeration with a value type other than int or str
    """

    class RGB(KeeNum):
      """RGB is a KeeNum enumeration for RGB colors."""
      RED = (255, 0, 0)
      GREEN = (0, 255, 0)
      BLUE = (0, 0, 255)

    self.assertIs(RGB((255, 0, 0)), RGB.RED)
    self.assertIs(RGB((0, 255, 0)), RGB.GREEN)
    self.assertIs(RGB((0, 0, 255)), RGB.BLUE)

  def test_bad_identifier_type(self) -> None:
    """
    Testing the errors raised when attempting to resolve a KeeNum member
    from unsupporterd identifier types.
    """

    class RGB(KeeNum):
      """RGB is a KeeNum enumeration for RGB colors."""
      RED = (255, 0, 0)
      GREEN = (0, 255, 0)
      BLUE = (0, 0, 255)

    with self.assertRaises(TypeException) as context:
      _ = RGB[42.0]
    e = context.exception
    self.assertEqual(e.varName, 'key')
    self.assertEqual(e.actualObject, 42.0)
    self.assertEqual(e.actualType, float)
    self.assertEqual(e.expectedType, (int, str, tuple))

  def test_bad_index(self) -> None:
    """
    Testing the errors raised when attempting to resolve a KeeNum member
    from an index that is out of range.
    """

    class RGB(KeeNum):
      """RGB is a KeeNum enumeration for RGB colors."""
      RED = (255, 0, 0)
      GREEN = (0, 255, 0)
      BLUE = (0, 0, 255)

    with self.assertRaises(IndexError) as context:
      _ = RGB[3]
    e = context.exception
    self.assertEqual(str(e), 'Index 3 out of range for RGB')

  def test_bad_value(self) -> None:
    """
    Testing the errors raised when attempting to resolve a KeeNum member
    from a value that does not match any member.
    """

    class RGB(KeeNum):
      """RGB is a KeeNum enumeration for RGB colors."""
      RED = (255, 0, 0)
      GREEN = (0, 255, 0)
      BLUE = (0, 0, 255)

    with self.assertRaises(ValueError) as context:
      _ = RGB[(69, 420, 1337)]
    e = context.exception
    self.assertEqual(str(e), '(69, 420, 1337)')

  def test_bad_name(self) -> None:
    """
    Testing the errors raised when attempting to resolve a KeeNum member
    from a name that does not match any member.
    """

    class RGB(KeeNum):
      """RGB is a KeeNum enumeration for RGB colors."""
      RED = (255, 0, 0)
      GREEN = (0, 255, 0)
      BLUE = (0, 0, 255)

    with self.assertRaises(KeyError) as context:
      _ = RGB['YELLOW']
    e = context.exception
    self.assertEqual(str(e), "'YELLOW'")  # KeyError message

  def test_str_repr(self) -> None:
    """
    Testing the string representation of a KeeNum enumeration.
    """

    class RGB(KeeNum):
      """RGB is a KeeNum enumeration for RGB colors."""
      RED = (255, 0, 0)
      GREEN = (0, 255, 0)
      BLUE = (0, 0, 255)

    self.assertEqual(str(RGB), 'RGB(KeeNum)[tuple]')
    self.assertEqual(str(RGB), repr(RGB))
    self.assertEqual(str(KeeNum), """<class 'KeeNum'>""")
    self.assertEqual(str(KeeNum), repr(KeeNum))
