"""
TestKeeFlagsMemberNames subclasses 'KeeTest' and pins that a 'KeeFlags'
class body may not use a name a member takes. A flag named 'NULL' made a
member of that name beside the empty member, so 'Odd.NULL' was the one
and 'Odd['NULL']' the other, and a class-body attribute such as
'READ_WRITE = 'rw'' beside the flags 'READ' and 'WRITE' was replaced by
the member of that name without a word.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.waitaminute.keenum import KeeFlagNameError, KeeMemberNameError

from . import KeeTest


class TestKeeFlagsMemberNames(KeeTest):
  """
  TestKeeFlagsMemberNames provides tests for names a member of a
  'KeeFlags' class takes.
  """

  def test_null_flag_refused(self) -> None:
    """A flag named 'NULL' raises, saying which member takes the name."""
    with self.assertRaises(KeeFlagNameError) as context:
      class Odd(KeeFlags):  # noqa: F841
        ONE = KeeFlag()
        NULL = KeeFlag()
    message = str(context.exception)
    self.assertIn("'NULL'", message)
    self.assertIn('no flag high', message)

  def test_member_name_refused(self) -> None:
    """A class-body attribute named as a member raises, naming it."""
    with self.assertRaises(KeeMemberNameError) as context:
      class Perm(KeeFlags):  # noqa: F841
        READ = KeeFlag()
        WRITE = KeeFlag()
        READ_WRITE = 'rw'
    exception = context.exception
    self.assertEqual(exception.memberName, 'READ_WRITE')
    self.assertEqual(exception.clsName, 'Perm')
    self.assertIn("'READ_WRITE'", str(exception))

  def test_attribute_before_flags_refused(self) -> None:
    """The attribute is refused before the flags it names too."""
    with self.assertRaises(KeeMemberNameError):
      class Perm(KeeFlags):  # noqa: F841
        READ_WRITE = 'rw'
        READ = KeeFlag()
        WRITE = KeeFlag()

  def test_null_attribute_refused(self) -> None:
    """A class-body attribute named 'NULL' takes the empty member's name."""
    with self.assertRaises(KeeMemberNameError):
      class Perm(KeeFlags):  # noqa: F841
        NULL = 0
        READ = KeeFlag()

  def test_other_names_kept(self) -> None:
    """A name no member takes stays a class attribute."""

    class Perm(KeeFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()
      LABEL = 'rw'
      WRITE_READ = 'wr'

    self.assertEqual(Perm.LABEL, 'rw')
    self.assertEqual(Perm.WRITE_READ, 'wr')
    self.assertIs(Perm['WRITE_READ'], Perm.READ_WRITE)
