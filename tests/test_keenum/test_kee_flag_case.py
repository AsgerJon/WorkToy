"""
TestKeeFlagCase subclasses 'KeeTest' and pins that a 'KeeFlags' class
body refuses a flag name that is not upper case with 'KeeCaseException',
as a 'KeeNum' body refuses a member name, while lookups by call or
subscript ignore case. The flags body used to accept any name, so
'Perm.read' became a member whose name broke the upper-case rule every
other enumeration name keeps.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.waitaminute.keenum import KeeCaseException

from . import KeeTest


class TestKeeFlagCase(KeeTest):
  """
  TestKeeFlagCase provides tests for the case of 'KeeFlags' flag names.
  """

  def test_lower_case_refused(self) -> None:
    """A lower-case flag name raises 'KeeCaseException' naming it."""
    with self.assertRaises(KeeCaseException) as context:
      class Perm(KeeFlags):
        read = KeeFlag()
    self.assertEqual(context.exception.name, 'read')
    self.assertIn("'read'", str(context.exception))

  def test_mixed_case_refused(self) -> None:
    """A mixed-case flag name raises 'KeeCaseException'."""
    with self.assertRaises(KeeCaseException):
      class Perm(KeeFlags):
        READ = KeeFlag()
        Write = KeeFlag()

  def test_upper_case_lookups_ignore_case(self) -> None:
    """Upper-case flag names are accepted, and lookups ignore case."""

    class Perm(KeeFlags):
      READ = KeeFlag()
      WRITE2 = KeeFlag()

    self.assertIs(Perm('read'), Perm.READ)
    self.assertIs(Perm['write2'], Perm.WRITE2)
