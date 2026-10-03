"""
TestFrozenBoxAttribute subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that a box declared in the body of a frozen EZData class
works as a class attribute. A box is a descriptor, not a field, and it
builds its default on the first read of an instance. It used to store that
default through the instance's '__setattr__', which a frozen class
generates to refuse every assignment, so the first read raised. The box
now stores through 'object.__setattr__', the way 'functools.cached_property'
writes past a frozen dataclass. Assigning or deleting the attribute stays
refused, since the frozen '__setattr__' and '__delattr__' run first.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeBox

from . import EZTest


class Weekday(KeeNum):
  """Weekday is the enumeration behind the 'KeeBox' attribute below."""

  MON = Kee[str]('mon')
  TUE = Kee[str]('tue')


class Frozen(EZData, frozen=True):
  """Frozen holds one field and one box of each kind."""

  x = EZField[int](0)
  tags = AttriBox[list]()
  fixed = FixBox[int](7)
  day = KeeBox[Weekday]('tue')


class TestFrozenBoxAttribute(EZTest):
  """
  TestFrozenBoxAttribute provides tests for boxes declared in the body of
  a frozen EZData class.
  """

  def test_attri_box_reads_default(self) -> None:
    """An 'AttriBox' builds its default on the first read."""
    self.assertEqual(Frozen().tags, [])

  def test_attri_box_default_per_instance(self) -> None:
    """Each instance builds a default of its own."""
    first, second = Frozen(), Frozen()
    self.assertIsNot(first.tags, second.tags)

  def test_fix_box_reads_default(self) -> None:
    """A 'FixBox' builds its default on the first read."""
    self.assertEqual(Frozen().fixed, 7)

  def test_kee_box_reads_default(self) -> None:
    """A 'KeeBox' resolves its default to the member."""
    self.assertIs(Frozen().day, Weekday.TUE)

  def test_assignment_refused(self) -> None:
    """Assigning the box attribute is refused by the frozen class."""
    frozen = Frozen()
    with self.assertRaises(AttributeError):
      frozen.tags = [1]
    self.assertEqual(frozen.tags, [])

  def test_deletion_refused(self) -> None:
    """Deleting the box attribute is refused by the frozen class."""
    frozen = Frozen()
    with self.assertRaises(AttributeError):
      del frozen.tags

  def test_box_is_no_field(self) -> None:
    """The boxes stay class attributes rather than fields, and an
    instance still compares by its one field."""
    self.assertEqual([f.fieldName for f in Frozen.fields], ['x'])
    self.assertEqual(Frozen(1), Frozen(1))
