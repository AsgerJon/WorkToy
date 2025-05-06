"""TestNewYeetDirectory tests the newDirectory function."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from test_work_io import BaseTest
from worktoy.text import monoSpace, wordWrap
from worktoy.waitaminute import PathSyntaxException
from worktoy.work_io import validateExistingDirectory, yeetDirectory
from worktoy.work_io import newDirectory, validateAvailablePath

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class TestNewYeetDirectory(BaseTest):
  """
  TestNewYeetDirectory tests the newDirectory function.
  """

  def test_new_yeet(self):
    """
    Test the newDirectory function.
    """
    #  Before creating the new directory
    self.assertFalse(os.path.exists(self.newDir))
    with self.assertRaises(FileNotFoundError) as context:
      yeetDirectory(self.newDir)
    #  Create the new directory
    newDir = newDirectory(self.newDir)
    #  After creating the new directory
    self.assertEqual(newDir, self.newDir)
    self.assertTrue(os.path.exists(self.newDir))
    self.assertTrue(os.path.isdir(self.newDir))
    with self.assertRaises(FileExistsError) as context:
      os.makedirs(self.newDir, exist_ok=False)
    #  Yeet the new directory
    yeetDirectory(self.newDir)
    #  After yeeting the new directory
    self.assertFalse(os.path.exists(self.newDir))
    with self.assertRaises(FileNotFoundError) as context:
      yeetDirectory(self.newDir)
