"""
TestBadNum tests that correct exceptions raise when KeeNum enumerations
are created with invalid values.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, auto, trust
from worktoy.waitaminute.keenum import KeeNumTypeException
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBadNum(KeeTest):
  """
  TestBadNum tests that correct exceptions raise when KeeNum enumerations
  are created with invalid values.
  """

  def test_bad_num(self) -> None:
    """
    Test that a KeeNum enumeration raises a ValueError when an invalid value
    is provided.
    """
    with self.assertRaises(KeeNumTypeException) as context:
      class BadType(KeeNum):
        """Inconsistent field types. """
        EIN = auto(1)
        ZWEI = auto(2)
        DREI = auto('3')
    e = context.exception
    self.assertEqual(e.memberName, 'DREI')
    self.assertEqual(e.memberValue, '3')
    self.assertEqual(e.expectedType, int)
    self.assertEqual(str(e), repr(e))

  def test_ignoring_decorated(self) -> None:
    """
    Test that a KeeNum enumeration raises a ValueError when an invalid value
    is provided, even when the class is decorated with @auto.
    """

    class IgnoringDecorated(KeeNum):
      """Inconsistent field types. """
      EIN = auto(1)
      ZWEI = auto(2)

      @trust
      def sus(self) -> None:
        """The '@trust' decorator makes the KeeNum class creation control
        flow ignore this method entirely."""

    with self.assertRaises(AttributeError) as context:
      IgnoringDecorated.sus()
    e = context.exception
    self.assertIn('has no attribute', str(e))
