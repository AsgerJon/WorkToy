"""
TestNum provides the basic tests for the KeeNum class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee, KeeMeta
from worktoy.waitaminute import TypeException, VariableNotNone
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from worktoy.waitaminute.keenum import KeeNameError, KeeIndexError
from worktoy.waitaminute.keenum import KeeMemberError, KeeDuplicate
from worktoy.waitaminute.keenum import KeeTypeException, KeeCaseException
from worktoy.waitaminute.keenum import KeeWriteOnceError
from . import KeeTest
from .examples import WeekDay, Compass, Brush, RGBNum, RootRGB, RGB, Dato, \
  Month

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestNum(KeeTest):
  """TestNum provides the basic tests for the KeeNum class."""

  def test_ad_hoc(self) -> None:
    """Test ad-hoc functionality."""

    for day in WeekDay:
      self.assertIsInstance(day, WeekDay)
      self.assertIsInstance(day, KeeNum)
      self.assertEqual(repr(day), str(day))

  def test_contains_members(self) -> None:
    """Test that the members of the WeekDay enumeration are as expected."""
    self.assertEqual(len(WeekDay), 7)
    self.assertIn(WeekDay.MONDAY, WeekDay)
    self.assertIn(WeekDay.TUESDAY, WeekDay)
    self.assertIn(WeekDay.WEDNESDAY, WeekDay)
    self.assertIn(WeekDay.THURSDAY, WeekDay)
    self.assertIn(WeekDay.FRIDAY, WeekDay)
    self.assertIn(WeekDay.SATURDAY, WeekDay)
    self.assertIn(WeekDay.SUNDAY, WeekDay)

  def test_contains_keys(self) -> None:
    """Tests that contains accepts keys as members"""
    for day in WeekDay:
      self.assertIn(day.name, WeekDay)

  def test_contains_indices(self) -> None:
    """Tests that contains accepts indices as members"""
    for day in WeekDay:
      self.assertIn(int(day), WeekDay)

  def test_bad_contains(self) -> None:
    """Tests that contains does not accept non-members."""
    self.assertNotIn('Mandag', WeekDay)
    self.assertNotIn('Tirsdag', WeekDay)
    self.assertNotIn('Onsdag', WeekDay)
    self.assertNotIn('Torsdag', WeekDay)
    self.assertNotIn('Fredag', WeekDay)
    self.assertNotIn('Lørdag', WeekDay)
    self.assertNotIn('Søndag', WeekDay)

  def test_keenum(self) -> None:
    """Test that the WeekDay class is a KeeNum."""
    self.assertIs(KeeNum.base, KeeNum)
    self.assertEqual(str(KeeNum), repr(KeeNum))
    self.assertEqual(str(WeekDay), repr(WeekDay))

  def test_is_instancecheck(self) -> None:
    for cls in self.exampleNums:
      self.assertIsInstance(cls, KeeMeta)
      for member in cls:
        self.assertIsInstance(member, cls)
        self.assertIsInstance(member, KeeNum)

  def test_is_subclasscheck(self) -> None:
    for cls in self.exampleNums:
      self.assertIsSubclass(cls, KeeNum)

  def test_is_not_instancecheck(self) -> None:
    """Test that the WeekDay class is not an instance of KeeNum."""
    items = [
      69,
      420.0,
      """Imma a KeeNum, trust me bro!""",
      type('Keeeeee', (), {}),
    ]
    for cls in self.exampleNums:
      for item in items:
        self.assertNotIsInstance(item, cls)
        self.assertNotIsInstance(item, KeeNum)

  def test_is_not_subclasscheck(self) -> None:
    """Test that the WeekDay class is not a subclass of KeeNum."""
    items = [
      int, float, str, type
    ]
    for cls in self.exampleNums:
      for item in items:
        self.assertNotIsSubclass(item, cls)
        self.assertNotIsSubclass(item, KeeNum)

  def test_bad_subclasscheck(self) -> None:
    """Test that the WeekDay class is not a subclass of KeeNum."""
    items = [
      69,
      420.0,
      """Imma a KeeNum, trust me bro!""",
    ]
    for cls in self.exampleNums:
      for item in items:
        with self.assertRaises(TypeError) as context:
          _ = issubclass(item, cls)
        e = context.exception
        e = context.exception
        self.assertIn('arg 1 must be a class', str(e))
        self.assertNotIsSubclass(type('imma a Kee, trust!', (), {}), cls)

  def test_good_resolve_member(self) -> None:
    """Test that the resolve_member method works as expected."""
    for day in WeekDay:
      self.assertIn(day, WeekDay)
      self.assertIn(day.name, WeekDay)
      self.assertIn(int(day), WeekDay)
    for i in range(69):
      for j, day in enumerate(WeekDay):
        self.assertIs(WeekDay[j - i * len(WeekDay)], day)

  def test_bad_resolve_member(self) -> None:
    """Test that the correct exception is raised when failing to resolve a
    member. """
    with self.assertRaises(KeeNameError) as context:
      _ = WeekDay['trololololo']
    e = context.exception
    self.assertIs(e.keenum, WeekDay)
    self.assertEqual(e.name, 'trololololo')
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(KeeIndexError) as context:
      _ = WeekDay[69420]
    e = context.exception
    self.assertIs(e.keenum, WeekDay)
    self.assertEqual(e.index, 69420)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(KeeMemberError) as context:
      _ = WeekDay[RootRGB.RED]
    e = context.exception
    self.assertIs(e.keenum, WeekDay)
    self.assertIs(e.member, RootRGB.RED)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(TypeException) as context:
      _ = WeekDay[0.8008135]
    e = context.exception
    self.assertEqual(e.varName, 'identifier')
    self.assertEqual(e.actualObject, 0.8008135)
    self.assertEqual(set(e.expectedTypes), {int, str, KeeNum})
    self.assertEqual(str(e), repr(e))

  def test_duplicate_exception(self) -> None:
    """Test that a duplicate exception is raised when creating an
    enumeration with duplicate members."""
    #  Testing duplicating member from base class
    breh = Kee[str]('breh')
    with self.assertRaises(KeeDuplicate) as context:
      class DuperTrooperIsLegend(WeekDay):
        MONDAY = breh
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, 'MONDAY')
    self.assertIs(e.oldMember, WeekDay.MONDAY.kee)
    self.assertIs(e.newMember, breh)

    #  Testing duplicating member in same class
    with self.assertRaises(KeeDuplicate) as context:
      a = Kee[str]('Mandag')
      b = Kee[str]('Tirsdag')

      class DuperTrooperIsLegend2(KeeNum):
        MONDAY = a
        MONDAY = b
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, 'MONDAY')
    self.assertIs(e.oldMember, a)
    self.assertIs(e.newMember, b)

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
    self.assertIs(WeekDay.MONDAY, WeekDay.__getattr__('MONDAY'))
    self.assertIs(WeekDay.TUESDAY, WeekDay.__getattr__('TUESDAY'))
    self.assertIs(WeekDay.WEDNESDAY, WeekDay.__getattr__('WEDNESDAY'))
    self.assertIs(WeekDay.THURSDAY, WeekDay.__getattr__('THURSDAY'))
    self.assertIs(WeekDay.FRIDAY, WeekDay.__getattr__('FRIDAY'))
    self.assertIs(WeekDay.SATURDAY, WeekDay.__getattr__('SATURDAY'))
    self.assertIs(WeekDay.SUNDAY, WeekDay.__getattr__('SUNDAY'))

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
    self.assertIs(WeekDay.MONDAY, WeekDay.monday)
    self.assertIs(WeekDay.TUESDAY, WeekDay.tuesday)
    self.assertIs(WeekDay.WEDNESDAY, WeekDay.wednesday)
    self.assertIs(WeekDay.THURSDAY, WeekDay.thursday)
    self.assertIs(WeekDay.FRIDAY, WeekDay.friday)
    self.assertIs(WeekDay.SATURDAY, WeekDay.saturday)
    self.assertIs(WeekDay.SUNDAY, WeekDay.sunday)

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

  def test_dato(self, ) -> None:
    """
    The 'Dato' class uses 'KeeNum' classes as attributes. This test aims
    at testing 'KeeNum' in a 'real-world' scenario rather than in a test
    coverage gymnastics type situation.
    """
    today = Dato.rightNow()
    self.assertIsInstance(today, Dato)
    self.assertIsInstance(today.year, int)
    self.assertIsInstance(today.month, Month)
    self.assertIsInstance(today.day, int)
    self.assertIsInstance(today.weekDay, WeekDay)
    self.assertEqual(today.datetimeDate, date.today())

    tomorrow = today.tomorrow()
    for _ in range(69):
      self.assertIsInstance(tomorrow, Dato)
      self.assertIsInstance(tomorrow.year, int)
      self.assertIsInstance(tomorrow.month, Month)
      self.assertIsInstance(tomorrow.day, int)
      self.assertIsInstance(tomorrow.weekDay, WeekDay)
      tomorrow = tomorrow.tomorrow()

    delta = tomorrow.datetimeDate - today.datetimeDate
    self.assertEqual(delta.days - 1, 69)

    yesterday = today.yesterday()
    for _ in range(420):
      self.assertIsInstance(yesterday, Dato)
      self.assertIsInstance(yesterday.year, int)
      self.assertIsInstance(yesterday.month, Month)
      self.assertIsInstance(yesterday.day, int)
      self.assertIsInstance(yesterday.weekDay, WeekDay)
      yesterday = yesterday.yesterday()

    delta = today.datetimeDate - yesterday.datetimeDate
    self.assertEqual(delta.days - 1, 420)

    greatScott = Dato(1985, Month.OCTOBER, 26)
    self.assertEqual(greatScott.year, 1985)
    self.assertIs(greatScott.month, Month.OCTOBER)
    self.assertEqual(greatScott.day, 26)
    self.assertIs(greatScott.weekDay, WeekDay.SATURDAY)
    self.assertIn('26. Oktober, 1985', str(greatScott))
    self.assertIn('Dato(1985, Month.OCTOBER, 26)', repr(greatScott))
