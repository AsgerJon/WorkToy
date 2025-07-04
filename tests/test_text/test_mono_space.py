"""TestMonoSpace tests the textFmt function."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import textFmt


class TestMonoSpace(TestCase):
  """TestMonoSpace tests the textFmt function."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

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
