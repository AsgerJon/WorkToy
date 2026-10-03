"""
TestKeeBoxIntIdentifier subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins how a 'KeeBox' resolves a lone 'int'. The 'int' names a
member by index when it is the index of a member, and no member has a
negative index, so a negative 'int' is a value: 'KeeBox[Status](-1)' is the
member whose value is '-1', where reading it as a position from the end
picks the last member instead. An 'int' that is no index is compared with
the member values only when it is an instance of their type. Otherwise the
value type converts it first, which is how '-1' finds the member whose
value is '-1.0', and how an 'int' never meets the '__eq__' of an 'RGB',
which raises on anything but a colour.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.waitaminute.keenum import KeeBoxValueError, KeeResolveError

from . import KeeTest
from .examples import ColorNum, WeekDay

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Status(KeeNum):
  """Status holds 'int' values, two of them negative. Read as positions
  from the end, '-1' and '-2' would name other members."""

  CRITICAL = Kee[int](-2)
  ERROR = Kee[int](-1)
  OK = Kee[int](0)
  WARN = Kee[int](1)


class Level(KeeNum):
  """Level holds 'float' values, one of them negative."""

  LOW = Kee[float](-1.0)
  ZERO = Kee[float](0.0)
  HIGH = Kee[float](1.0)


class TestKeeBoxIntIdentifier(KeeTest):
  """
  TestKeeBoxIntIdentifier provides tests for a 'KeeBox' resolving a lone
  'int', given as the default or assigned.
  """

  @staticmethod
  def _boxDefault(num: Any, identifier: Any) -> Any:
    """Returns what a 'KeeBox' over 'num' holds when given 'identifier' as
    its default."""

    class Holder:
      field = KeeBox[num](identifier)

    return Holder().field

  def test_negative_value_resolves(self) -> None:
    """
    A negative 'int' resolves to the member holding it as its value, as
    the default and by assignment alike.
    """
    self.assertIs(self._boxDefault(Status, -1), Status.ERROR)
    self.assertIs(self._boxDefault(Status, -2), Status.CRITICAL)

    class Holder:
      field = KeeBox[Status](Status.OK)

    holder = Holder()
    holder.field = -1
    self.assertIs(holder.field, Status.ERROR)
    holder.field = -2
    self.assertIs(holder.field, Status.CRITICAL)

  def test_negative_value_matching_no_member(self) -> None:
    """
    A negative 'int' that is the value of no member raises
    'KeeBoxValueError', like any other value matching no member, whether
    or not it would count as a position from the end.
    """
    for identifier in (-3, -10):
      with self.subTest(identifier=identifier):
        with self.assertRaises(KeeBoxValueError):
          self._boxDefault(Status, identifier)

  def test_negative_int_converts_to_value_type(self) -> None:
    """
    A negative 'int' given to a box over 'Level', whose values are
    'float', is converted by the value type and finds the member whose
    value is '-1.0'.
    """
    self.assertIs(self._boxDefault(Level, -1), Level.LOW)

  def test_negative_int_is_no_index(self) -> None:
    """
    A negative 'int' given to a box whose enumeration holds values of
    another type is no index either, and matches no member.
    """
    for num in (WeekDay, ColorNum):
      with self.subTest(num=num.__name__):
        with self.assertRaises(KeeBoxValueError):
          self._boxDefault(num, -1)

  def test_int_beyond_members_meets_no_foreign_eq(self) -> None:
    """
    An 'int' past the last index reaches the values of 'ColorNum' only
    as an 'RGB' built from it, so the '__eq__' of 'RGB' never meets the
    bare 'int', and the lookup ends in 'KeeBoxValueError'.
    """
    with self.assertRaises(KeeBoxValueError):
      self._boxDefault(ColorNum, 99)

  def test_index_of_member(self) -> None:
    """
    An 'int' that is the index of a member names that member, before any
    lookup by value: '0' is the first member of 'Status', although the
    value of 'Status.OK' is '0'.
    """
    self.assertIs(self._boxDefault(Status, 0), Status.CRITICAL)
    self.assertIs(self._boxDefault(Status, 3), Status.WARN)
    self.assertIs(self._boxDefault(WeekDay, 6), WeekDay.SUNDAY)

  def test_member_count_is_no_index(self) -> None:
    """
    The number of members is one past the last index, so it is looked up
    as a value, and matching no member it raises 'KeeBoxValueError'.
    """
    with self.assertRaises(KeeBoxValueError):
      self._boxDefault(Status, len(Status))

  def test_bool_is_refused(self) -> None:
    """
    A 'bool' is neither an index nor a value of an 'int' enumeration, so
    the box refuses it as calling the enumeration does.
    """
    with self.assertRaises(KeeResolveError):
      Status(True)
    with self.assertRaises(KeeResolveError):
      self._boxDefault(Status, True)
