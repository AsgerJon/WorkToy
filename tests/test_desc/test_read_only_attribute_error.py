"""
TestReadOnlyAttributeError subclasses 'DescTest' and pins that a refused
write to a read-only attribute, and a refused deletion, are
'AttributeError's, as Python's own refusals are: a property without a
setter, a named tuple field, a frozen dataclass through
'FrozenInstanceError'. Code written against those catches
'AttributeError' to skip what cannot be set, and a worktoy descriptor
should be skipped the same way. 'QuickDesc' already refuses with an
'AttributeError', but a bare one of its own, where every other descriptor
raises 'ReadOnlyError' and 'ProtectedError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field, AttriBox
from worktoy.mcls import BaseObject
from worktoy.utilities import ExceptionInfo
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError

from . import DescTest


class Form(BaseObject):
  """
  Form is filled from a posted dict. 'summary' is derived, so a posted
  value for it is skipped, as a read-only property would be.
  """

  name = AttriBox[str]('')
  age = AttriBox[int](0)
  summary = Field()

  @summary.GET
  def _getSummary(self) -> str:
    return '%s (%d)' % (self.name, self.age)

  def load(self, posted: dict) -> list:
    """Fills the fields from 'posted' and returns the keys skipped
    because they could not be set."""
    skipped = []
    for key, value in posted.items():
      try:
        setattr(self, key, value)
      except AttributeError:
        skipped.append(key)
    return skipped


class TestReadOnlyAttributeError(DescTest):
  """
  TestReadOnlyAttributeError provides tests for the refusals of a write
  to, and a deletion of, a read-only attribute.
  """

  def test_form_load_skips_derived(self) -> None:
    """A posted value for the derived field is skipped, and the other two
    fields are set."""
    form = Form()
    skipped = form.load({'name': 'Ada', 'age': 36, 'summary': 'ignored'})
    self.assertEqual(skipped, ['summary'])
    self.assertEqual(form.name, 'Ada')
    self.assertEqual(form.age, 36)
    self.assertEqual(form.summary, 'Ada (36)')

  def test_write_refused_as_attribute_error(self) -> None:
    """Writing the derived field raises an 'AttributeError'."""
    with self.assertRaises(AttributeError):
      Form().summary = 'x'

  def test_delete_refused_as_attribute_error(self) -> None:
    """Deleting the derived field raises an 'AttributeError'."""
    with self.assertRaises(AttributeError):
      del Form().summary

  def test_read_only_error_is_attribute_error(self) -> None:
    """'ReadOnlyError' is an 'AttributeError', as 'AccessError' is."""
    self.assertIsSubclass(ReadOnlyError, AttributeError)

  def test_protected_error_is_attribute_error(self) -> None:
    """'ProtectedError' is an 'AttributeError', as 'AccessError' is."""
    self.assertIsSubclass(ProtectedError, AttributeError)

  def test_refusals_keep_their_own_types(self) -> None:
    """The refusals are still caught by their own names."""
    with self.assertRaises(ReadOnlyError):
      Form().summary = 'x'
    with self.assertRaises(ProtectedError):
      del Form().summary

  def test_quick_desc_write_is_read_only_error(self) -> None:
    """'QuickDesc' refuses a write with 'ReadOnlyError', as every other
    descriptor does."""
    with self.assertRaises(ReadOnlyError):
      ExceptionInfo().report = 'edited'

  def test_quick_desc_delete_is_protected_error(self) -> None:
    """'QuickDesc' refuses a deletion with 'ProtectedError', as every
    other descriptor does."""
    with self.assertRaises(ProtectedError):
      del ExceptionInfo().report

  def test_quick_desc_refusals_are_attribute_errors(self) -> None:
    """'QuickDesc' refusals are 'AttributeError's, as the five tests of
    'QuickDesc' have always said."""
    with self.assertRaises(AttributeError):
      ExceptionInfo().report = 'edited'
    with self.assertRaises(AttributeError):
      del ExceptionInfo().report
