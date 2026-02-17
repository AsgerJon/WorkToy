"""
TestSubclassException tests the SubclassException class from the
'worktoy.waitaminute' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import WaitAMinuteTest
from worktoy.waitaminute import SubclassException

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSubclassException(WaitAMinuteTest):
  """
  TestSubclassException tests the SubclassException class from the
  'worktoy.waitaminute' module.
  """

  def test_base(self) -> None:
    """
    Tests that the SubclassException correctly subclasses TypeError itself.
    """
    self.assertTrue(issubclass(SubclassException, TypeError))

  def test_verbatim(self) -> None:
    """
    Since the SubclassException is not raised directly anywhere in the
    functional code, the test must raise it explicitly.
    """
    with self.assertRaises(SubclassException) as context:
      raise SubclassException(int, tuple)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.expected, tuple)
    self.assertEqual(e.cls, int)
