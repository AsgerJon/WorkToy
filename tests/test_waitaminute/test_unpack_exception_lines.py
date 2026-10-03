"""
TestUnpackExceptionLines subclasses 'WaitAMinuteTest' and pins that the
message of 'UnpackException' lists the arguments on lines of their own.
It wrote them with newline characters, which 'textFmt' collapses to
spaces, so the message ran on one line.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import UnpackException

from . import WaitAMinuteTest


class TestUnpackExceptionLines(WaitAMinuteTest):
  """
  TestUnpackExceptionLines provides tests for the lines of the message of
  'UnpackException'.
  """

  def test_one_argument_per_line(self) -> None:
    """Each argument stands indented on a line of its own."""
    lines = str(UnpackException(69, 420)).splitlines()
    self.assertEqual(lines[0], "'unpack' found no iterable argument from:")
    self.assertEqual(lines[1:3], ['  69', '  420'])
    self.assertTrue(lines[3].startswith('and is running in strict mode'))
