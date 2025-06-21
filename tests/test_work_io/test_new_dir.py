"""
TestNewDir tests the creation of new directories with the work_io module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.parse import maybe
from worktoy.work_io import newDirectory

from . import BaseTest

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Any


class TestNewDir(BaseTest):
  """
  TestNewDir tests the creation of new directories with the work_io module.
  """

  def setUp(self, ) -> None:
    """
    Set up the test environment by clearing the temporary directory.
    """
    super().setUp()
    pathComponents = """never gonna give you up""".split()
    self.newPath = os.path.join(self.tempDir, *pathComponents)

  def test_new(self, ) -> None:
    """
    This method first creates a new directory at the 'newPath'. Next it
    attempts to create it again, expecting a 'FileExistsError' to be raised.
    """
    #  Test that temp directory is empty
    for item in os.listdir(self.testDir):
      if item != os.path.basename(self.testFile):
        infoSpec = """Expected temporary directory '%s' to contain only 
        the test file '%s', but found '%s'!"""
        info = infoSpec % (self.testDir, self.testFile, item)
        raise AssertionError(info)

    #  Create a new directory
    newPath = newDirectory(self.newPath)

    #  Test that the new directory exists
    if not os.path.exists(newPath):
      infoSpec = """Expected new directory '%s' to exist, but it does not!"""
      info = infoSpec % newPath
      raise AssertionError(info)

    #  Test that the new directory is a directory
    if not os.path.isdir(newPath):
      infoSpec = """Expected new directory '%s' to be a directory, but it 
      is not!"""
      info = infoSpec % newPath
      raise AssertionError(info)

    #  Attempt to create the same directory again
    with self.assertRaises(FileExistsError) as context:
      newDirectory(self.newPath)

    #  Test that the exception message is correct
    self.assertIn('already exists', str(context.exception), )
    for component in self.newPath.split(os.sep):
      if component:
        self.assertIn(component, str(context.exception), )
