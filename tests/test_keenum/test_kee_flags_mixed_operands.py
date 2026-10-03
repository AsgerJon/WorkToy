"""
TestKeeFlagsMixedOperands subclasses 'KeeTest' and pins that the bitwise
operators of 'KeeFlags' members take members of the very same class
only. A member of a derived class passes the 'isinstance' check, so
'Perm.READ | More.EXEC' looked up a combination 'Perm' does not have and
raised a raw 'KeyError'; it now raises the 'TypeError' Python raises for
unsupported operands, as the other order already did.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag

from . import KeeTest


class Perm(KeeFlags):
  """Perm holds two flags."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class More(Perm):
  """More adds a flag to 'Perm'."""

  EXEC = KeeFlag()


class TestKeeFlagsMixedOperands(KeeTest):
  """
  TestKeeFlagsMixedOperands provides tests for operators between members
  of a flags class and of a class derived from it.
  """

  def test_mixed_classes_refused(self) -> None:
    """Each operator raises 'TypeError' for a member of the derived
    class, in either order."""
    left, right = Perm.READ, More.EXEC
    for operation in (
        lambda a, b: a | b,
        lambda a, b: a & b,
        lambda a, b: a ^ b,
    ):
      with self.assertRaises(TypeError):
        operation(left, right)
      with self.assertRaises(TypeError):
        operation(right, left)

  def test_same_class(self) -> None:
    """The operators combine members of the same class."""
    self.assertIs(Perm.READ | Perm.WRITE, Perm.READ_WRITE)
    self.assertIs(More.READ | More.EXEC, More.READ_EXEC)
    self.assertIs(More.READ_EXEC & More.EXEC, More.EXEC)
    self.assertIs(More.READ ^ More.READ_EXEC, More.EXEC)
