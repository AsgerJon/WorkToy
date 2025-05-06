"""TestKeeNum - Test the KeeNum class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import auto, KeeNum

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class WeekDay(KeeNum):
  """WeekDay enumeration."""

  MONDAY = auto('Monday')
  TUESDAY = auto('Tuesday')
  WEDNESDAY = auto('Wednesday')
  THURSDAY = auto('Thursday')
  FRIDAY = auto('Friday')
  SATURDAY = auto('Saturday')
  SUNDAY = auto('Sunday')


class Ugedag(KeeNum):
  """Ugedag enumeration."""

  MONDAY = auto('Mandag')
  TUESDAY = auto('Tirsdag')
  WEDNESDAY = auto('Onsdag')
  THURSDAY = auto('Torsdag')
  FRIDAY = auto('Fredag')
  SATURDAY = auto('Lørdag')
  SUNDAY = auto('Søndag')


class Wochentag(KeeNum):
  """Wochentag enumeration."""

  MONDAY = auto('Montag')
  TUESDAY = auto('Dienstag')
  WEDNESDAY = auto('Mittwoch')
  THURSDAY = auto('Donnerstag')
  FRIDAY = auto('Freitag')
  SATURDAY = auto('Samstag')
  SUNDAY = auto('Sonntag')


class TestKeeNum(TestCase):
  """Test the KeeNum class."""

  def test_auto(self) -> None:
    """Test the auto function."""
    self.assertEqual(len(WeekDay), len(Ugedag))
    self.assertEqual(len(Ugedag), len(Wochentag))

  def test_resolve_indices(self, ) -> None:
    """Tests that the indices are resolved correctly."""
    for i, (day, dag, tag) in enumerate(zip(WeekDay, Ugedag, Wochentag)):
      self.assertEqual(day.index, i)
      self.assertEqual(dag.index, i)
      self.assertEqual(tag.index, i)

  def test_resolve_keys(self, ) -> None:
    """Tests that the values are resolved correctly."""
    keys = [day.baseName for day in WeekDay]
    for (key, day, dag, tag) in zip(keys, WeekDay, Ugedag, Wochentag):
      self.assertEqual(day.key, key)
      self.assertEqual(dag.key, key)
      self.assertEqual(tag.key, key)
