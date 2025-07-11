"""
TestExistingDirValidator tests the ExistingDirValidator class from the
'worktoy.work_io' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

import sys

from unittest import TestCase

from . import WorkIOTest
from tests import WYD
from worktoy.waitaminute import PathSyntaxException
from worktoy.work_io import validateExistingDirectory


class TestExistingDirValidator(WorkIOTest):
  """TestExistingDirValidator tests the existing directory validator."""

  @classmethod
  def tearDownClass(cls) -> None:
    super().tearDownClass()
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_dir(self) -> None:
    """Test the existing directory validator."""
    validateExistingDirectory(self.tempDir)
    validateExistingDirectory(self.testDir)
    validateExistingDirectory(self.emptyDir)

  def test_bad_dir(self) -> None:
    """Test the existing directory validator with a bad directory."""
    with self.assertRaises(FileNotFoundError) as context:
      validateExistingDirectory(self.emptyPath)

  def test_malformed_dir(self) -> None:
    """Test the error raised on a malformed directory."""
    with self.assertRaises(PathSyntaxException) as context:
      validateExistingDirectory('imma dir, trust me bro!')
    e = context.exception
    self.assertEqual(repr(e), str(e))

  def test_file(self, ) -> None:
    """Test the existing directory validator with a file."""
    for tempFile in self.tempFiles:
      with self.assertRaises(NotADirectoryError) as context:
        validateExistingDirectory(tempFile)

  def test_file_not_strict(self) -> None:
    """Test the existing directory validator with a file in non-strict
    mode."""
    for tempFile in self.tempFiles:
      self.assertFalse(validateExistingDirectory(tempFile, strict=False), )
