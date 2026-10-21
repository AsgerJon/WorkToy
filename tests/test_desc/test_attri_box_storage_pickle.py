"""
TestAttriBoxStoragePickle subclasses 'DescTest' from the 'tests.test_desc'
package and pins that the storage names of box fields are stable strings,
so an instance pickled with its field values comes back holding them, two
near names included. A storage name derived from the identity of a box
would not survive a round trip, and the fields of an unpickled instance
would rebuild their defaults in silence.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest


class Account(BaseObject):
  """Account declares two near-named fields the tests pickle."""

  fooBar = AttriBox[int](1)
  foo_bar = AttriBox[str]('s')


def _roundTrip(obj):
  return pickle.loads(pickle.dumps(obj))


class TestAttriBoxStoragePickle(DescTest):
  """
  TestAttriBoxStoragePickle provides tests for the field values of a
  pickled instance.
  """

  def test_values_survive(self) -> None:
    """Both written values come back on the unpickled instance."""
    account = Account()
    account.fooBar = 7
    account.foo_bar = 'x'
    back = _roundTrip(account)
    self.assertIsNot(back, account)
    self.assertEqual(back.fooBar, 7)
    self.assertEqual(back.foo_bar, 'x')

  def test_storage_names_survive(self) -> None:
    """The unpickled instance holds the values under the storage names
    the field names derive."""
    account = Account()
    account.fooBar = 7
    account.foo_bar = 'x'
    back = _roundTrip(account)
    self.assertEqual(back.__dict__['__fooBar__attribox_field_object__'], 7)
    self.assertEqual(back.__dict__['__foo_bar__attribox_field_object__'], 'x')

  def test_unread_field_builds_after(self) -> None:
    """A field never read before pickling is built on the first read
    after, while a field written before keeps the written value."""
    account = Account()
    account.fooBar = 7
    back = _roundTrip(account)
    self.assertEqual(back.fooBar, 7)
    self.assertEqual(back.foo_bar, 's')
