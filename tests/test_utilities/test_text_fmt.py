"""TestMonoSpace tests the textFmt function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from . import UtilitiesTest
from worktoy.utilities import textFmt


class TestMonoSpace(UtilitiesTest):
  """TestMonoSpace tests the textFmt function."""

  def test_textFmt(self) -> None:
    """Test the textFmt function."""

    sample = """This is a multi-line 
    string  with a lot of spaces!!"""
    actual = textFmt(sample)
    sampleSpaceless = sample.replace(' ', '').replace('\n', '')
    actualSpaceless = actual.replace(' ', '').replace('\n', '')
    self.assertEqual(sampleSpaceless, actualSpaceless)

  def test_lineBreak(self) -> None:
    """Tests if textFmt correctly inserts line breaks """
    sample = """This is the first line, <br>and this is the second line."""
    expected = """This is the first line, \nand this is the second line."""
    actual = textFmt(sample)
    self.assertEqual(expected, actual)

  def test_tabs(self) -> None:
    """Tests if textFmt correctly inserts multiple space in place of
    <tab>."""
    sample = """Left:<tab>Right"""
    expected = """Left:  Right"""
    actual = textFmt(sample)
    self.assertEqual(expected, actual)

  def test_empty(self) -> None:
    """Tests if textFmt returns an empty string when given an empty
    string."""
    self.assertEqual(textFmt(), '')
    self.assertEqual(textFmt(''), '')

  def test_empty_strings(self) -> None:
    """
    Tests multiple arguments to textFmt that include blank lines.
    """
    actual = textFmt('foo', str(), 'bar')
    expected = 'foo bar'
    self.assertEqual(expected, actual)

  def test_non_str(self) -> None:
    """Tests if textFmt raises a TypeError when given a non-string
    input."""
    expected = '69 420 1337'
    actual = textFmt(69, 420, 1337)
    self.assertEqual(expected, actual)
