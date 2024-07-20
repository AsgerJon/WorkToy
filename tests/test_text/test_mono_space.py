"""TestMonoSpace tests the monoSpace function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.text import monoSpace


class TestMonoSpace(TestCase):
  """TestMonoSpace tests the monoSpace function."""

  def test_monoSpace(self) -> None:
    """Test the monoSpace function."""

    sample = """This is a multi-line 
    string  with a lot of spaces!!"""
    actual = monoSpace(sample)
    sampleSpaceless = sample.replace(' ', '').replace('\n', '')
    actualSpaceless = actual.replace(' ', '').replace('\n', '')
    self.assertEqual(sampleSpaceless, actualSpaceless)

  def test_lineBreak(self) -> None:
    """Tests if monoSpace correctly inserts line breaks """
    sample = """This is the first line, <br>and this is the second line. """
    expected = """This is the first line,\nand this is the second line."""
    actual = monoSpace(sample)
    self.assertEqual(expected, actual)

  def test_tabs(self) -> None:
    """Tests if monoSpace correctly inserts multiple space in place of
    <tab>."""
    sample = """Left:<tab>Right"""
    expected = """Left:  Right"""
    actual = monoSpace(sample)
    self.assertEqual(expected, actual)
