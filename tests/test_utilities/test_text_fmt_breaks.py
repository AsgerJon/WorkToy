"""
TestTextFmtBreaks subclasses 'UtilitiesTest' and pins that 'textFmt' drops
the space on either side of a line break. It kept them, so a line ended in
a space, and a '<br>' at the end of a source line left the next line
starting with one, as in the message of 'DuplicateSignature'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import textFmt

from . import UtilitiesTest


class TestTextFmtBreaks(UtilitiesTest):
  """
  TestTextFmtBreaks provides tests for the spaces around a '<br>'.
  """

  def test_space_before_break(self) -> None:
    """No line ends in the space written before the break."""
    actual = textFmt('first line, <br>second line', newLineSymbol='\n')
    self.assertEqual(actual, 'first line,\nsecond line')

  def test_space_after_break(self) -> None:
    """No line starts with the space written after the break."""
    actual = textFmt('first line<br> second line', newLineSymbol='\n')
    self.assertEqual(actual, 'first line\nsecond line')

  def test_source_line_end(self) -> None:
    """A break closing a source line leaves the next line unindented."""
    sample = """first line:<br>
    second line"""
    actual = textFmt(sample, newLineSymbol='\n')
    self.assertEqual(actual, 'first line:\nsecond line')

  def test_tab_kept(self) -> None:
    """A tab after the break still indents the next line."""
    actual = textFmt('first <br> <tab>second', newLineSymbol='\n')
    self.assertEqual(actual, 'first\n  second')
