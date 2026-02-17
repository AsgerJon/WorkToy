"""
TestIllegalInstantiation tests the IllegalInstantiation class from the
'worktoy.waitaminute' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import WaitAMinuteTest
from worktoy.core.sentinels import THIS
from worktoy.waitaminute.meta import IllegalInstantiation

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestIllegalInstantiation(WaitAMinuteTest):
  """
  TestIllegalInstantiation tests the IllegalInstantiation class from the
  'worktoy.waitaminute' module.
  """

  def test_base(self) -> None:
    """
    Tests that the IllegalInstantiation correctly subclasses TypeError
    itself.
    """
    self.assertTrue(issubclass(IllegalInstantiation, TypeError))

  def test_raises(self) -> None:
    """
    Tests that the IllegalInstantiation raises an exception with the
    correct message.
    """
    with self.assertRaises(IllegalInstantiation) as context:
      _ = THIS()
    e = context.exception
    self.assertEqual(str(e), repr(e))
