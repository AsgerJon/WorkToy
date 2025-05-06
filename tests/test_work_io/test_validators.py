"""TestValidators tests the validators in the work_io module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from test_work_io import BaseTest
from worktoy.text import monoSpace, wordWrap
from worktoy.waitaminute import PathSyntaxException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass

from worktoy.work_io import validateExistingDirectory, validateAvailablePath

from worktoy.work_io import validateExistingFile


class TestValidators(BaseTest):
  """TestValidators tests the validators in the work_io module."""

  def test_validateExistingDirectory(self) -> None:
    """Test validateExistingDirectory."""
    validated = validateExistingDirectory(self.tempDir)
    self.assertEqual(validated, self.tempDir)
    with self.assertRaises(FileNotFoundError):
      validateExistingDirectory(self.susDir)
    with self.assertRaises(NotADirectoryError):
      validateExistingDirectory(self.testFile)

  def test_validateExistingFile(self) -> None:
    """Test validateExistingFile."""
    validated = validateExistingFile(self.testFile)
    self.assertEqual(validated, self.testFile)
    with self.assertRaises(FileNotFoundError):
      validateExistingFile(self.susFile)
    with self.assertRaises(IsADirectoryError):
      validateExistingFile(self.testDir)

  def test_validateAvailablePath(self) -> None:
    """Test validateAvailablePath."""
    validated = validateAvailablePath(self.newFile)
    self.assertEqual(validated, self.newFile)
    with self.assertRaises(FileExistsError):
      validateAvailablePath(self.testFile)
    with self.assertRaises(PathSyntaxException):
      validateAvailablePath('trolololo...')
