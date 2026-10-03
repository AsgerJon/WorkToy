"""
TestKeeMetaKeeNumHint subclasses 'KeeTest' and pins that an enumeration
offers no 'keeNum' attribute. 'KeeMeta' declared one as a 'Field' without
a getter, only so a type checker saw it, which made 'WeekDay.keeNum'
raise 'AccessError' from a descriptor that should not have been there.
The root of a metaclass is still read off the metaclass, as
'KeeMeta.keeNum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeMeta, KeeNum, Kee
from worktoy.waitaminute.desc import AccessError

from . import KeeTest


class WeekDay(KeeNum):
  """WeekDay is a small enumeration."""

  MONDAY = Kee[int](1)


class TestKeeMetaKeeNumHint(KeeTest):
  """
  TestKeeMetaKeeNumHint provides tests for 'keeNum' on an enumeration.
  """

  def test_no_attribute(self) -> None:
    """'keeNum' on an enumeration raises 'AttributeError', not
    'AccessError'."""
    with self.assertRaises(AttributeError) as context:
      _ = WeekDay.keeNum
    self.assertNotIsInstance(context.exception, AccessError)

  def test_metaclass_root(self) -> None:
    """The root is read off the metaclass."""
    self.assertIs(KeeMeta.keeNum, KeeNum)
