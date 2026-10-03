"""
TestBaseTestSubclassMsg subclasses 'BaseTest' and pins that
'assertIsSubclass' and 'assertNotIsSubclass' report the 'msg' they are
given. Before Python 3.14, which adds both to 'TestCase', 'BaseTest'
supplies them, and its versions dropped 'msg'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest


class TestBaseTestSubclassMsg(BaseTest):
  """
  TestBaseTestSubclassMsg provides tests for the 'msg' of the subclass
  assertions.
  """

  def test_is_subclass_msg(self) -> None:
    """A failing 'assertIsSubclass' reports the message."""
    with self.assertRaises(AssertionError) as context:
      self.assertIsSubclass(int, str, msg='custom message')
    self.assertIn('custom message', str(context.exception))

  def test_not_is_subclass_msg(self) -> None:
    """A failing 'assertNotIsSubclass' reports the message."""
    with self.assertRaises(AssertionError) as context:
      self.assertNotIsSubclass(bool, int, msg='custom message')
    self.assertIn('custom message', str(context.exception))
