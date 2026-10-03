"""
TestPickleException subclasses 'WaitAMinuteTest' from the
'tests.test_waitaminute' package and pins 'PickleException', which every
object defined by 'worktoy' raises when it is pickled, or when a pickle
stream tries to restore state into it. It is a 'TypeError', as the refusal
Python raises for an object it cannot pickle, and it refuses to be pickled
itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy.waitaminute import PickleException

from . import WaitAMinuteTest


class Foo:
  """Foo stands in for the object a refusal is about."""


class TestPickleException(WaitAMinuteTest):
  """
  TestPickleException provides tests for 'PickleException'.
  """

  def test_type_error(self) -> None:
    """'PickleException' is a 'TypeError'."""
    self.assertIsSubclass(PickleException, TypeError)

  def test_attributes(self) -> None:
    """The exception holds the object and the refused action."""
    foo = Foo()
    exception = PickleException(foo, 'pickled')
    self.assertIs(exception.obj, foo)
    self.assertEqual(exception.action, 'pickled')

  def test_message(self) -> None:
    """The message names the type of the object and the action."""
    info = str(PickleException(Foo(), 'unpickled'))
    self.assertIn("'Foo'", info)
    self.assertIn('unpickled', info)

  def test_refuses_pickling(self) -> None:
    """The exception refuses to be pickled itself."""
    with self.assertRaises(PickleException):
      pickle.dumps(PickleException(Foo(), 'pickled'))
