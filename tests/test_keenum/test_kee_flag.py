"""
TestKeeFlag provides tests specifically for the entry class KeeFlag.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeFlag
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeFlag(KeeTest):
  """TestKeeFlag provides tests specifically for the entry class KeeFlag."""

  def testImplementedEqualityOperator(self, ) -> None:
    """
    Tests the equality operator for situations other than
    'NotImplemented'.
    """

    for cls in self.exampleFlags:
      for left in cls.flags:
        for right in cls.flags:
          if left.index == right.index:
            self.assertTrue(left == right)
          else:
            self.assertFalse(left == right)

  def testNotImplementedEqualityOperator(self, ) -> None:
    """
    Tests the equality operator for situations resulting in
    'NotImplemented'.
    """
    for leftCls in self.exampleFlags:
      for rightCls in self.exampleFlags:
        for left in leftCls.flags:
          for right in rightCls.flags:
            if leftCls == rightCls:
              if left.index == right.index:
                self.assertTrue(left == right)
              else:
                self.assertFalse(left == right)
            else:
              expected = NotImplemented
              leftActual = KeeFlag.__eq__(left, right, _debug=True)
              rightActual = KeeFlag.__eq__(right, left, _debug=True)
              self.assertIs(leftActual, expected)
              self.assertIs(rightActual, expected)
