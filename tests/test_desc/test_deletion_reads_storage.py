"""
TestDeletionReadsStorage subclasses 'DescTest' from the 'tests.test_desc'
package and pins that deleting a descriptor never builds a value. Before
deleting, 'Object.__delete__' reads the old value, only to report it. That
read used to build the default of an unset box and store it, which for a
'FixBox' is its single write: the deletion was refused with
'ProtectedError', and a later first assignment raised 'WriteOnceError'
against a default nobody asked for. An 'AttriBox' built a default only to
overwrite it with 'DELETED', and a default that failed to build made the
deletion fail. The read now passes '_deleting=True', and the boxes answer
it from their storage alone, so an unset field reports no old value. A
'Field' answers the read through its getter, which runs once, and its
'ProtectedError' reports what the getter returned; it used to run the
getter twice, once for that read and once more for the error.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox, Field
from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ProtectedError

from . import DescTest


class Counted:
  """Counted counts how many times it is built."""

  __built__ = 0

  def __init__(self, ) -> None:
    type(self).__built__ += 1


class Broken:
  """Broken fails to build."""

  def __init__(self, ) -> None:
    raise ValueError('cannot build')


class Color(KeeNum):
  """Color is the enumeration behind the 'KeeBox' fields below."""

  RED = Kee[str]('red')
  BLUE = Kee[str]('blue')


class Owner(BaseObject):
  """Owner holds one descriptor of each kind the tests delete."""

  __getter_calls__ = 0

  fixed = FixBox[int](7)
  counted = AttriBox[Counted]()
  broken = AttriBox[Broken]()
  color = KeeBox[Color]('purple')
  protected = Field()
  deletable = Field()

  @protected.GET
  def _getProtected(self) -> int:
    type(self).__getter_calls__ += 1
    return 3

  @deletable.GET
  def _getDeletable(self) -> int:
    return 5

  @deletable.DELETE
  def _deleteDeletable(self) -> None:
    pass


class TestDeletionReadsStorage(DescTest):
  """
  TestDeletionReadsStorage provides tests for deleting descriptors whose
  value was never read or built.
  """

  def test_fix_box_write_survives_refusal(self) -> None:
    """A caught refusal to delete a 'FixBox' leaves its one write
    available."""
    owner = Owner()
    try:
      del owner.fixed
    except ProtectedError:
      pass
    owner.fixed = 42
    self.assertEqual(owner.fixed, 42)

  def test_fix_box_default_after_refusal(self) -> None:
    """A 'FixBox' refused its deletion still builds its default on the
    first read."""
    owner = Owner()
    with self.assertRaises(ProtectedError):
      del owner.fixed
    self.assertEqual(owner.fixed, 7)

  def test_fix_box_refusal_reports_no_value(self) -> None:
    """Refusing to delete an unset 'FixBox' reports no old value."""
    with self.assertRaises(ProtectedError) as context:
      del Owner().fixed
    self.assertIsNone(context.exception.oldVal)

  def test_fix_box_refusal_keeps_value(self) -> None:
    """Refusing to delete a written 'FixBox' keeps and reports its
    value."""
    owner = Owner()
    owner.fixed = 5
    with self.assertRaises(ProtectedError) as context:
      del owner.fixed
    self.assertEqual(context.exception.oldVal, 5)
    self.assertEqual(owner.fixed, 5)

  def test_reading_builds(self) -> None:
    """A read, unlike a deletion, does build the default: 'Counted' once,
    while 'Broken' fails to build."""
    before = Counted.__built__
    _ = Owner().counted
    self.assertEqual(Counted.__built__, before + 1)
    with self.assertRaises(TypeError):
      _ = Owner().broken

  def test_attri_box_builds_nothing(self) -> None:
    """Deleting an unset 'AttriBox' builds no default, and the field then
    reads as missing."""
    owner = Owner()
    before = Counted.__built__
    del owner.counted
    self.assertEqual(Counted.__built__, before)
    with self.assertRaises(MissingVariable):
      _ = owner.counted

  def test_attri_box_broken_default_deletes(self) -> None:
    """An 'AttriBox' whose default fails to build can still be deleted."""
    owner = Owner()
    del owner.broken
    with self.assertRaises(MissingVariable):
      _ = owner.broken

  def test_kee_box_broken_default_deletes(self) -> None:
    """A 'KeeBox' whose default resolves to no member can still be
    deleted."""
    owner = Owner()
    del owner.color
    with self.assertRaises(MissingVariable):
      _ = owner.color

  def test_deleted_twice(self) -> None:
    """Deleting a field that is already deleted raises
    'MissingVariable'."""
    owner = Owner()
    del owner.counted
    with self.assertRaises(MissingVariable):
      del owner.counted

  def test_field_getter_runs_once(self) -> None:
    """Refusing to delete a 'Field' without deleters runs the getter once,
    for the old value the refusal reports."""
    owner = Owner()
    self.assertEqual(owner.protected, 3)
    before = Owner.__getter_calls__
    with self.assertRaises(ProtectedError) as context:
      del owner.protected
    self.assertEqual(Owner.__getter_calls__, before + 1)
    self.assertEqual(context.exception.oldVal, 3)

  def test_field_deleter_runs(self) -> None:
    """A 'Field' with a deleter and a getter taking only 'self' deletes
    without complaint."""
    owner = Owner()
    self.assertEqual(owner.deletable, 5)
    del owner.deletable
