"""
TestKeeFlagsValueDiamond subclasses 'KeeTest' and pins that the value of
a 'KeeFlags' member comes from the '_getValue' the ordinary method
resolution order finds. 'KeeFlagsMeta' used to write the getter it chose
onto every flags class, so a class inheriting a getter seemed to define
it itself, and in a diamond 'class Both(Left, Right)' the getter of the
common base, written onto 'Left', beat the override of 'Right'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag

from . import KeeTest


class Base(KeeFlags):
  """Base has a getter of its own."""

  A = KeeFlag()

  def _getValue(self) -> str:
    return 'base'


class Left(Base):
  """Left inherits the getter of 'Base'."""


class Right(Base):
  """Right overrides the getter."""

  def _getValue(self) -> str:
    return 'right'


class Both(Left, Right):
  """Both inherits from 'Left' and 'Right'."""


class TestKeeFlagsValueDiamond(KeeTest):
  """
  TestKeeFlagsValueDiamond provides tests for the getter of the member
  values in a diamond of flags classes.
  """

  def test_diamond_takes_override(self) -> None:
    """'Both' takes the getter of 'Right', which comes before 'Base' in
    its method resolution order."""
    self.assertEqual(Both.A.value, 'right')

  def test_inherited_getter_not_written(self) -> None:
    """A class inheriting the getter does not hold one of its own."""
    self.assertNotIn('_getValue', Left.__dict__)
    self.assertNotIn('_getValue', Both.__dict__)

  def test_each_class_value(self) -> None:
    """Each class reads the getter it resolves."""
    self.assertEqual(Base.A.value, 'base')
    self.assertEqual(Left.A.value, 'base')
    self.assertEqual(Right.A.value, 'right')
