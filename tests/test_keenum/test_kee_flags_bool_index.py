"""
TestKeeFlagsBoolIndex subclasses 'KeeTest' and pins that a 'bool' is no
index or value of a 'KeeFlags' class, as it is none for a 'KeeNum' of
'int' values. A 'bool' is an 'int', so 'Perm(True)' used to be the
member of index 1 and 'Perm[False]' the member of index 0.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.waitaminute.keenum import KeeResolveError

from . import KeeTest


class Perm(KeeFlags):
  """Perm holds two flags."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class TestKeeFlagsBoolIndex(KeeTest):
  """
  TestKeeFlagsBoolIndex provides tests for a 'bool' given to a flags
  class.
  """

  def test_call_refuses_bool(self) -> None:
    """A call or subscript with a 'bool' matches no member."""
    for identifier in (True, False):
      with self.subTest(identifier=identifier):
        with self.assertRaises(KeeResolveError):
          Perm(identifier)
        with self.assertRaises(KeeResolveError):
          _ = Perm[identifier]

  def test_int_index(self) -> None:
    """An 'int' is still an index."""
    self.assertIs(Perm(1), Perm.READ)
    self.assertIs(Perm[0], Perm.NULL)

  def test_bool_valued_flags(self) -> None:
    """A 'bool' still finds a member of 'bool' value."""

    class Switch(KeeFlags):
      ON = KeeFlag()

      def _getValue(self) -> bool:
        return True if self.index else False

    self.assertIs(Switch(True), Switch.ON)
