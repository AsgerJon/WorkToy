"""
TestMemberMethodCalls subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that a method written in the body of a 'KeeNum' or a
'KeeFlags' class is called on a member as Python calls any method: it
receives its positional parameters by keyword too, and a positional
argument beyond those it declares raises 'TypeError' instead of being
dropped.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag

from . import KeeTest


class TestMemberMethodCalls(KeeTest):
  """
  TestMemberMethodCalls provides tests for calling methods on members of
  'KeeNum' and 'KeeFlags' enumerations.
  """

  @staticmethod
  def _buildLevel() -> type:
    """The '_buildLevel' method builds a fresh 'KeeNum' enumeration with
    a method written in its class body."""

    class Level(KeeNum):
      LOW = Kee[int](1)
      HIGH = Kee[int](2)

      def scaled(self, factor: int) -> int:
        return self.value * factor

    return Level

  @staticmethod
  def _buildPerm() -> type:
    """The '_buildPerm' method builds a fresh 'KeeFlags' enumeration with
    a method written in its class body."""

    class Perm(KeeFlags):
      READ = KeeFlag()
      WRITE = KeeFlag()

      def grants(self, flagName: str) -> bool:
        return True if flagName in self.names else False

    return Perm

  def test_kee_num_method_takes_keyword(self) -> None:
    """A 'KeeNum' member method receives its parameter by keyword."""
    level = self._buildLevel()
    self.assertEqual(level.HIGH.scaled(factor=3), 6)

  def test_kee_num_method_refuses_extra(self) -> None:
    """A 'KeeNum' member method raises 'TypeError' for a positional
    argument beyond those it declares."""
    level = self._buildLevel()
    with self.assertRaises(TypeError):
      level.HIGH.scaled(3, 4)

  def test_kee_flags_method_takes_keyword(self) -> None:
    """A 'KeeFlags' member method receives its parameter by keyword."""
    perm = self._buildPerm()
    self.assertTrue(perm.READ_WRITE.grants(flagName='READ'))

  def test_kee_flags_method_refuses_extra(self) -> None:
    """A 'KeeFlags' member method raises 'TypeError' for a positional
    argument beyond those it declares."""
    perm = self._buildPerm()
    with self.assertRaises(TypeError):
      perm.READ_WRITE.grants('READ', 'WRITE')

  def test_methods_as_declared(self) -> None:
    """Member methods called as declared answer as before."""
    level, perm = self._buildLevel(), self._buildPerm()
    self.assertEqual(level.LOW.scaled(5), 5)
    self.assertTrue(perm.READ.grants('READ'))
    self.assertFalse(perm.READ.grants('WRITE'))
