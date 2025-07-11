"""
TestNewYeetDirectory tests the newDirectory and scrapDirectory functions
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from . import WorkIOTest
from tests import WYD
from worktoy.work_io import validateExistingDirectory, scrapDirectory
from worktoy.work_io import newDirectory, validateAvailablePath

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestNewYeetDirectory(WorkIOTest):
  """TestNewYeetDirectory tests the newDirectory and scrapDirectory
  functions."""

  @classmethod
  def tearDownClass(cls) -> None:
    super().tearDownClass()
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_new_scrap_directory(self) -> None:
    """
    newDirectory creates a new directory, and scrapDirectory removes it.
    """
    newDir = os.path.join(self.tempDir, 'new_scrap_dir')
    self.assertEqual(validateAvailablePath(newDir), newDir, )
    newDirectory(newDir)
    self.assertEqual(validateExistingDirectory(newDir), newDir, )
    scrapDirectory(newDir)
    self.assertFalse(scrapDirectory(newDir, strict=False), )

  def test_new_unavailable_directory(self) -> None:
    """
    newDirectory raises FileExistsError if the directory already exists.
    """
    for tempDir in (self.tempDir, self.testDir, self.emptyDir):
      with self.assertRaises(FileExistsError) as context:
        newDirectory(tempDir)

  def test_scrap_non_existing(self) -> None:
    """Testing scrapDirectory with a non-existing directory."""
    for i in range(10):
      trollDir = os.path.join(self.emptyDir, 'trololololo%d' % i)
      with self.assertRaises(FileNotFoundError) as context:
        scrapDirectory(trollDir)

  def test_scrap_file(self) -> None:
    """Testing scrapDirectory with a file."""
    for tempFile in self.tempFiles:
      with self.assertRaises(NotADirectoryError) as context:
        scrapDirectory(tempFile)
      e = context.exception
      expected = """The path received by """, """is not a directory!"""
      for expectedPart in expected:
        self.assertIn(expectedPart, str(e), )
