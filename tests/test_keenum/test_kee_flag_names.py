"""
TestKeeFlagNames subclasses 'KeeTest' from the 'tests.test_keenum' package
and pins the naming rules of 'KeeFlags'. A flag name may not contain an
underscore, since the name of a combined member joins its flag names
with underscores: the flags 'READ', 'ONLY' and 'READ_ONLY' would give two
members the name 'READ_ONLY'. The class body fails at the offending line
with 'KeeFlagNameError'. With the underscore kept for joining, a lookup
by name ignores both case and order, and that includes 'NULL'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.waitaminute.keenum import KeeFlagNameError

from . import KeeTest


class Perm(KeeFlags):
  """Perm declares two single-bit flags."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class TestKeeFlagNames(KeeTest):
  """
  TestKeeFlagNames provides tests for the names of 'KeeFlags' flags and
  members.
  """

  def test_underscore_in_flag_name_raises(self) -> None:
    """
    A flag named with an underscore raises 'KeeFlagNameError' while the
    class is being built. The exception is a 'ValueError', like
    'KeeCaseException', and names the class and the flag.
    """
    with self.assertRaises(KeeFlagNameError) as context:
      class Access(KeeFlags):  # noqa: F841
        WRITE = KeeFlag()
        READ_ONLY = KeeFlag()
    e = context.exception
    self.assertIsInstance(e, ValueError)
    self.assertEqual(e.clsName, 'Access')
    self.assertEqual(e.name, 'READ_ONLY')
    self.assertIn('Access', str(e))
    self.assertIn('READ_ONLY', str(e))
    self.assertEqual(str(e), repr(e))

  def test_ambiguous_names_refused(self) -> None:
    """
    The flags 'READ', 'ONLY' and 'READ_ONLY' would give two members the
    name 'READ_ONLY'. The class is refused at the third flag.
    """
    with self.assertRaises(KeeFlagNameError) as context:
      class Clash(KeeFlags):  # noqa: F841
        READ = KeeFlag()
        ONLY = KeeFlag()
        READ_ONLY = KeeFlag()
    self.assertEqual(context.exception.name, 'READ_ONLY')

  def test_underscore_in_subclass_raises(self) -> None:
    """
    A subclass adding a flag named with an underscore is refused the
    same way.
    """
    with self.assertRaises(KeeFlagNameError) as context:
      class MorePerm(Perm):  # noqa: F841
        READ_ONLY = KeeFlag()
    self.assertEqual(context.exception.clsName, 'MorePerm')

  def test_combined_names_ignore_case_and_order(self) -> None:
    """
    A combined member is found by its flag names in any case and in any
    order.
    """
    for name in ('READ_WRITE', 'read_write', 'Write_Read'):
      with self.subTest(name=name):
        self.assertIs(Perm[name], Perm.READ_WRITE)

  def test_null_ignores_case(self) -> None:
    """
    'NULL' is found in any case, by subscript, by call and by 'in'.
    """
    for name in ('NULL', 'null', 'Null'):
      with self.subTest(name=name):
        self.assertIs(Perm[name], Perm.NULL)
        self.assertIs(Perm(name), Perm.NULL)
        self.assertIn(name, Perm)
