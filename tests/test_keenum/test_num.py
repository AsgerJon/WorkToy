"""
TestNum provides the basic tests for the KeeNum class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee, KeeMeta
from worktoy.waitaminute import TypeException, VariableNotNone
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from worktoy.waitaminute.keenum import KeeNameError, KeeIndexError
from worktoy.waitaminute.keenum import KeeMemberError, KeeDuplicate
from worktoy.waitaminute.keenum import KeeTypeException, KeeCaseException
from worktoy.waitaminute.keenum import KeeWriteOnceError
from . import KeeTest
from .examples import RootRGB, RGB, Brush, RGBNum

if TYPE_CHECKING:  # pragma: no cover
  pass


class Weekday(KeeNum):
  """Weekday enumeration."""
  MONDAY = Kee[str]('Mandag')
  TUESDAY = Kee[str]('Tirsdag')
  WEDNESDAY = Kee[str]('Onsdag')
  THURSDAY = Kee[str]('Torsdag')
  FRIDAY = Kee[str]('Fredag')
  SATURDAY = Kee[str]('Lørdag')
  SUNDAY = Kee[str]('Søndag')


class Compass(KeeNum):
  """Compass enumeration."""
  NULL = Kee[complex](0 + 0j)  # Falsy because of name being 'NULL'
  ALSO_NULL = Kee[complex](0 + 0j)  # Falsy because of value
  EAST = Kee[complex](1 + 0j)
  NORTH = Kee[complex](0 + 1j)
  WEST = Kee[complex](-1 + 0j)
  SOUTH = Kee[complex](0 - 1j)
  NORTHEAST = Kee[complex](1 + 1j)
  NORTHWEST = Kee[complex](-1 + 1j)
  SOUTHEAST = Kee[complex](1 - 1j)
  SOUTHWEST = Kee[complex](-1 - 1j)


class TestNum(KeeTest):
  """TestNum provides the basic tests for the KeeNum class."""

  def test_ad_hoc(self) -> None:
    """Test ad-hoc functionality."""

    for day in Weekday:
      self.assertIsInstance(day, Weekday)
      self.assertIsInstance(day, KeeNum)
      self.assertEqual(repr(day), str(day))

  def test_contains_members(self) -> None:
    """Test that the members of the Weekday enumeration are as expected."""
    self.assertEqual(len(Weekday), 7)
    self.assertIn(Weekday.MONDAY, Weekday)
    self.assertIn(Weekday.TUESDAY, Weekday)
    self.assertIn(Weekday.WEDNESDAY, Weekday)
    self.assertIn(Weekday.THURSDAY, Weekday)
    self.assertIn(Weekday.FRIDAY, Weekday)
    self.assertIn(Weekday.SATURDAY, Weekday)
    self.assertIn(Weekday.SUNDAY, Weekday)

  def test_contains_keys(self) -> None:
    """Tests that contains accepts keys as members"""
    for day in Weekday:
      self.assertIn(day.name, Weekday)

  def test_contains_indices(self) -> None:
    """Tests that contains accepts indices as members"""
    for day in Weekday:
      self.assertIn(int(day), Weekday)

  def test_bad_contains(self) -> None:
    """Tests that contains does not accept non-members."""
    self.assertNotIn('Mandag', Weekday)
    self.assertNotIn('Tirsdag', Weekday)
    self.assertNotIn('Onsdag', Weekday)
    self.assertNotIn('Torsdag', Weekday)
    self.assertNotIn('Fredag', Weekday)
    self.assertNotIn('Lørdag', Weekday)
    self.assertNotIn('Søndag', Weekday)

  def test_keenum(self) -> None:
    """Test that the Weekday class is a KeeNum."""
    self.assertIs(KeeNum.base, KeeNum)
    self.assertEqual(str(KeeNum), repr(KeeNum))
    self.assertEqual(str(Weekday), repr(Weekday))

  def test_good_instancecheck(self) -> None:
    self.assertIsInstance(Weekday, KeeMeta)

  def test_good_subclasscheck(self) -> None:
    self.assertIsSubclass(Weekday, KeeNum)

  def test_bad_instancecheck(self) -> None:
    """Test that the Weekday class is not an instance of KeeNum."""
    self.assertNotIsInstance("""Imma a KeeNum, trust me bro!""", KeeMeta)
    self.assertNotIsInstance(type('imma a Kee, trust!', (), {}), KeeMeta)

  def test_bad_subclasscheck(self) -> None:
    """Test that the Weekday class is not a subclass of KeeNum."""
    self.assertNotIsSubclass("""Imma a KeeNum, trust me bro!""", KeeNum)
    self.assertNotIsSubclass(type('imma a Kee, trust!', (), {}), KeeNum)

  def test_good_resolve_member(self) -> None:
    """Test that the resolve_member method works as expected."""
    for day in Weekday:
      self.assertIn(day, Weekday)
      self.assertIn(day.name, Weekday)
      self.assertIn(int(day), Weekday)
    for i in range(69):
      for j, day in enumerate(Weekday):
        self.assertIs(Weekday[j - i * len(Weekday)], day)

  def test_bad_resolve_member(self) -> None:
    """Test that the correct exception is raised when failing to resolve a
    member. """
    with self.assertRaises(KeeNameError) as context:
      _ = Weekday['trololololo']
    e = context.exception
    self.assertIs(e.keenum, Weekday)
    self.assertEqual(e.name, 'trololololo')
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(KeeIndexError) as context:
      _ = Weekday[69420]
    e = context.exception
    self.assertIs(e.keenum, Weekday)
    self.assertEqual(e.index, 69420)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(KeeMemberError) as context:
      _ = Weekday[RootRGB.RED]
    e = context.exception
    self.assertIs(e.keenum, Weekday)
    self.assertIs(e.member, RootRGB.RED)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(TypeException) as context:
      _ = Weekday[0.8008135]
    e = context.exception
    self.assertEqual(e.varName, 'identifier')
    self.assertEqual(e.actualObject, 0.8008135)
    self.assertEqual(set(e.expectedTypes), {int, str, KeeNum})
    self.assertEqual(str(e), repr(e))

  def test_duplicate_exception(self) -> None:
    """Test that a duplicate exception is raised when creating an
    enumeration with duplicate members."""
    #  Testing duplicating member from base class
    with self.assertRaises(KeeDuplicate) as context:
      class DuperTrooperIsLegend(Weekday):
        MONDAY = Kee[str]('breh')
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, 'MONDAY')
    self.assertEqual(e.value.getValue(), 'breh')

    #  Testing duplicating member in same class
    with self.assertRaises(KeeDuplicate) as context:
      class DuperTrooperIsLegend2(KeeNum):
        MONDAY = Kee[str]('Mandag')
        MONDAY = Kee[str]('Mandag')
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, 'MONDAY')
    self.assertEqual(e.value.getValue(), 'Mandag')

  def test_bad_type(self) -> None:
    """Test that a NotImplementedError is raised when the member type is not
    a KeeNum."""
    with self.assertRaises(KeeTypeException) as context:
      class BadType(KeeNum):
        BAD = Kee[int](42)
        TO = Kee[RGB](255, 255, 255)
    e = context.exception
    self.assertEqual(e.name, 'TO')
    self.assertEqual(e.value, RGB(255, 255, 255))
    self.assertEqual(set(e.expectedTypes), {int, })
    self.assertEqual(str(e), repr(e))

  def test_coverage_gymnastics(self) -> None:
    """Covers the hard-to-reach parts of the code."""
    breh = Kee[int](69)
    with self.assertRaises(KeeCaseException) as context:
      breh.name = 'lmao'
    e = context.exception
    self.assertEqual(e.name, 'lmao')
    self.assertEqual(str(e), repr(e))

    breh.name = 'LMAO'
    with self.assertRaises(VariableNotNone) as context:
      breh.name = 'YOLO'
    e = context.exception
    self.assertEqual(e.name, 'name')
    self.assertEqual(e.value, 'LMAO')
    self.assertEqual(str(e), repr(e))

    class Breh(KeeNum):
      FOO = Kee[int](69)
      BAR = Kee[int]('420')

    self.assertEqual(Breh.FOO.value, 69)
    self.assertEqual(Breh.BAR.value, 420)

    self.assertEqual(Breh.FOO, Breh.FOO)
    self.assertNotEqual(Breh.FOO, Breh.BAR)
    self.assertNotEqual(Breh.FOO, 'RED breh!')

    with self.assertRaises(KeeWriteOnceError) as context:
      setattr(Breh.FOO, 'lmao', True)
    e = context.exception
    self.assertIs(e.keenum, Breh)
    self.assertEqual(e.member, Breh.FOO)
    self.assertEqual(e.attribute, 'lmao')
    self.assertEqual(str(e), repr(e))

  def test_class_variable_num(self) -> None:
    """Test that the class variable 'num' is set correctly."""
    brushTest = Brush()
    self.assertIsInstance(brushTest, Brush)

    class Foo:
      colorNum = RGBNum.RED

    foo = Foo()

    with self.assertRaises(ReadOnlyError) as context:
      foo.colorNum = 'breh'
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo.colorNum)
    self.assertEqual(e.newVal, 'breh')
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(ProtectedError) as context:
      del foo.colorNum
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo.colorNum)
    self.assertIs(e.oldVal, RGBNum.RED)
    self.assertEqual(str(e), repr(e))

  def test_getattr(self, ) -> None:
    """Tests the getattr method."""
    self.assertIs(Weekday.MONDAY, Weekday.__getattr__('MONDAY'))
    self.assertIs(Weekday.TUESDAY, Weekday.__getattr__('TUESDAY'))
    self.assertIs(Weekday.WEDNESDAY, Weekday.__getattr__('WEDNESDAY'))
    self.assertIs(Weekday.THURSDAY, Weekday.__getattr__('THURSDAY'))
    self.assertIs(Weekday.FRIDAY, Weekday.__getattr__('FRIDAY'))
    self.assertIs(Weekday.SATURDAY, Weekday.__getattr__('SATURDAY'))
    self.assertIs(Weekday.SUNDAY, Weekday.__getattr__('SUNDAY'))

    self.assertIs(Compass.EAST, Compass.__getattr__('EAST'))
    self.assertIs(Compass.NORTH, Compass.__getattr__('NORTH'))
    self.assertIs(Compass.WEST, Compass.__getattr__('WEST'))
    self.assertIs(Compass.SOUTH, Compass.__getattr__('SOUTH'))
    self.assertIs(Compass.NORTHEAST, Compass.__getattr__('NORTHEAST'))
    self.assertIs(Compass.NORTHWEST, Compass.__getattr__('NORTHWEST'))
    self.assertIs(Compass.SOUTHEAST, Compass.__getattr__('SOUTHEAST'))
    self.assertIs(Compass.SOUTHWEST, Compass.__getattr__('SOUTHWEST'))

  def test_getattr_hard(self, ) -> None:
    """Tests the case-insensitive getattr method."""
    self.assertIs(Weekday.MONDAY, Weekday.monday)
    self.assertIs(Weekday.TUESDAY, Weekday.tuesday)
    self.assertIs(Weekday.WEDNESDAY, Weekday.wednesday)
    self.assertIs(Weekday.THURSDAY, Weekday.thursday)
    self.assertIs(Weekday.FRIDAY, Weekday.friday)
    self.assertIs(Weekday.SATURDAY, Weekday.saturday)
    self.assertIs(Weekday.SUNDAY, Weekday.sunday)

    self.assertIs(Compass.EAST, Compass.east)
    self.assertIs(Compass.NORTH, Compass.north)
    self.assertIs(Compass.WEST, Compass.west)
    self.assertIs(Compass.SOUTH, Compass.south)
    self.assertIs(Compass.NORTHEAST, Compass.northeast)
    self.assertIs(Compass.NORTHWEST, Compass.northwest)
    self.assertIs(Compass.SOUTHEAST, Compass.southeast)
    self.assertIs(Compass.SOUTHWEST, Compass.southwest)

  def test_from_value(self) -> None:
    """Tests the from_value method."""
    self.assertIs(Compass.fromValue(1 + 0j), Compass.EAST)
    self.assertIs(Compass.fromValue(0 + 1j), Compass.NORTH)
    self.assertIs(Compass.fromValue(-1 + 0j), Compass.WEST)
    self.assertIs(Compass.fromValue(0 - 1j), Compass.SOUTH)
    self.assertIs(Compass.fromValue(1 + 1j), Compass.NORTHEAST)
    self.assertIs(Compass.fromValue(-1 + 1j), Compass.NORTHWEST)
    self.assertIs(Compass.fromValue(1 - 1j), Compass.SOUTHEAST)
    self.assertIs(Compass.fromValue(-1 - 1j), Compass.SOUTHWEST)

  def test_from_value_hard(self, ) -> None:
    """Tests calling the class such that it falls back to 'fromValue'."""
    self.assertIs(Compass(1 + 0j), Compass.EAST)
    self.assertIs(Compass(0 + 1j), Compass.NORTH)
    self.assertIs(Compass(-1 + 0j), Compass.WEST)
    self.assertIs(Compass(0 - 1j), Compass.SOUTH)
    self.assertIs(Compass(1 + 1j), Compass.NORTHEAST)
    self.assertIs(Compass(-1 + 1j), Compass.NORTHWEST)
    self.assertIs(Compass(1 - 1j), Compass.SOUTHEAST)
    self.assertIs(Compass(-1 - 1j), Compass.SOUTHWEST)

  def test_bool(self, ) -> None:
    """Tests the bool method."""
    for direction in Compass:
      if direction in [Compass.NULL, Compass.ALSO_NULL]:
        self.assertFalse(direction)
      else:
        self.assertTrue(direction)
