"""
TestKeeMultipleBasesMessage subclasses 'KeeTest' and pins that the
message refusing an enumeration with several enumeration bases lists the
bases indented on lines of their own. They were joined with the tab ahead
of the line break, so each line but the last ended in the tab.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee

from . import KeeTest


class First(KeeNum):
  """First has one member."""
  X = Kee[int](1)


class Second(KeeNum):
  """Second has another."""
  Y = Kee[int](2)


class TestKeeMultipleBasesMessage(KeeTest):
  """
  TestKeeMultipleBasesMessage provides tests for the lines of the message
  refusing several enumeration bases.
  """

  def test_bases_indented(self) -> None:
    """Each base stands indented on a line of its own."""
    with self.assertRaises(ValueError) as context:
      class Both(First, Second):  # noqa: F841
        pass
    lines = str(context.exception).splitlines()
    self.assertEqual(lines[1:], ['  First', '  Second'])
