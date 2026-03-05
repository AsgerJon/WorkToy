"""
TestAvailablePathValidator tests the AvailablePathValidator class from the
'worktoy.work_io' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import WorkIOTest
from worktoy.waitaminute import PathSyntaxException
from worktoy.work_io import validateAvailablePath


class TestAvailablePathValidator(WorkIOTest):
  """TestAvailablePathValidator tests the available path validator."""

  @classmethod
  def tearDownClass(cls) -> None:
    """Set up the test class by creating a temporary directory."""
    super().tearDownClass()
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_empty_path(self) -> None:
    """Test the available path validator with an empty path."""
    self.assertEqual(validateAvailablePath(self.emptyPath), self.emptyPath, )

  def test_file_path(self) -> None:
    """Test the available path validator with a file path."""
    for tempFile in self.tempFiles:
      with self.assertRaises(FileExistsError) as context:
        _ = validateAvailablePath(tempFile)
      e = context.exception
      self.assertIn('already exists', str(e))

  def test_file_path_non_strict(self) -> None:
    """Test the available path validator with a file path in non-strict
    mode."""
    for tempFile in self.tempFiles:
      self.assertFalse(validateAvailablePath(tempFile, strict=False))

  def test_validate_malformed_path(self) -> None:
    """Test the available path validator with a malformed path."""
    with self.assertRaises(PathSyntaxException) as context:
      validateAvailablePath('imma a path, trust!')
    e = context.exception
    self.assertEqual(repr(e), str(e))

  def test_existing_dir_path(self) -> None:
    """Test the available path validator with a directory path."""
    with self.assertRaises(FileExistsError) as context:
      validateAvailablePath(self.tempDir)
    with self.assertRaises(FileExistsError) as context:
      validateAvailablePath(self.testDir)
    with self.assertRaises(FileExistsError) as context:
      validateAvailablePath(self.emptyDir)

  def test_available_dir_path(self) -> None:
    """Test the available path validator with an available directory path."""
    emp = self.emptyPath
    self.assertEqual(validateAvailablePath(emp), emp)
