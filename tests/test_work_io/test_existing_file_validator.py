"""
TestExistingFileValidator tests the functionality of the existing file
validator in the work_io module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

import sys

from unittest import TestCase

from . import BaseTest
from tests import WYD
from worktoy.waitaminute import PathSyntaxException
from worktoy.work_io import validateExistingFile


class TestExistingFileValidator(BaseTest):
  """TestExistingFileValidator tests the existing file validator."""

  @classmethod
  def tearDownClass(cls) -> None:
    super().tearDownClass()
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_file(self) -> None:
    """Test the existing file validator."""
    for tempFile in self.tempFiles:
      self.assertEqual(validateExistingFile(tempFile), tempFile)

  def test_bad_file(self) -> None:
    """Test the existing file validator with a bad file."""
    with self.assertRaises(FileNotFoundError) as context:
      validateExistingFile(self.emptyPath)

  def test_malformed_file(self) -> None:
    """Test the error raised on a malformed file."""
    with self.assertRaises(PathSyntaxException) as context:
      validateExistingFile('imma file, trust me bro!')
    e = context.exception
    self.assertEqual(repr(e), str(e))

  def test_is_dir(self) -> None:
    """Test the existing file validator with a directory."""
    for dirPath in (self.tempDir, self.testDir, self.emptyDir):
      with self.assertRaises(IsADirectoryError) as context:
        validateExistingFile(dirPath)
      e = context.exception
      self.assertIn('is not a file', str(e))

  def test_is_dir_not_strict(self) -> None:
    """Test the existing file validator with a directory in non-strict
    mode."""
    for dirPath in (self.tempDir, self.testDir, self.emptyDir):
      self.assertFalse(validateExistingFile(dirPath, strict=False), )
