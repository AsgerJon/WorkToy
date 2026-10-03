"""
TestKeeEmptyLookup subclasses 'KeeTest' and pins that a lookup on an
enumeration without members raises 'KeeResolveError', the documented
miss of every lookup. Past the name lookup, a lookup used to ask for the
value type, which an enumeration without members has none of, and so
raised a plain 'TypeError' instead.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest


class Empty(KeeNum):
  """Empty declares no members."""


class TestKeeEmptyLookup(KeeTest):
  """
  TestKeeEmptyLookup provides tests for lookups on an enumeration without
  members.
  """

  def test_call(self) -> None:
    """A call raises 'KeeResolveError'."""
    for identifier in ('x', 0, 1.5):
      with self.subTest(identifier=identifier):
        with self.assertRaises(KeeResolveError):
          Empty(identifier)

  def test_subscript(self) -> None:
    """A subscript raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      _ = Empty[0]

  def test_from_value(self) -> None:
    """'fromValue' raises 'KeeResolveError'."""
    with self.assertRaises(KeeResolveError):
      Empty.fromValue(1)

  def test_value_type_still_refused(self) -> None:
    """Asking for the value type itself still raises 'TypeError', since
    there is none."""
    with self.assertRaises(TypeError):
      _ = Empty.valueType
