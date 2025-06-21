"""BaseTest provides a baseclass for testing the 'worktoy.work_io' module.
It subclasses the unittest.TestCase class and adds file functionality."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class TempDir:
  """
  Provides a temporary directory for testing implemented with the
  descriptor protocol.
  """

  @staticmethod
  def _getPath() -> str:
    """
    Returns the path to the temporary directory.
    """
    return os.path.join(os.getcwd(), 'temp')

  def __get__(self, instance: Any, owner: type) -> str:
    """
    Returns the path to the temporary directory.
    """
    return self._getPath()


class BaseTest(TestCase):
  """
  BaseTest provides a baseclass for testing the 'worktoy.work_io' module.
  It subclasses the unittest.TestCase class and adds file functionality.
  """

  tempDir = TempDir()

  @classmethod
  def clearTempDir(cls) -> None:
    """
    Clears the temporary directory.
    """
    if os.path.exists(cls.tempDir):
      for root, dirs, files in os.walk(cls.tempDir, topdown=False):
        for name in files:
          os.remove(os.path.join(root, name))
        for name in dirs:
          os.rmdir(os.path.join(root, name))
      os.rmdir(cls.tempDir)
    os.makedirs(cls.tempDir, exist_ok=True)

  @classmethod
  def setUpClass(cls) -> None:
    """
    Set up the test case.
    """
    if os.path.exists(cls.tempDir):
      cls.clearTempDir()
    os.makedirs(cls.tempDir, exist_ok=True)
    cls.testDir = os.path.join(cls.tempDir, "test_dir")
    cls.testFile = os.path.join(cls.testDir, "test_file.txt")
    cls.newFile = os.path.join(cls.tempDir, "new_file.txt")
    cls.newDir = os.path.join(cls.tempDir, "new_dir")
    cls.susDir = os.path.join(cls.testDir, "trolololo...")
    cls.susFile = os.path.join(cls.testDir, "trolololo.txt")
    os.makedirs(cls.testDir, exist_ok=True)
    f = 'pycharm, please!'
    try:
      f = open(cls.testFile, 'w')
    except Exception as exception:
      infoSpec = """The file '%s' could not be created!"""
      info = monoSpace(infoSpec % cls.testFile)
      raise OSError(info) from exception
    else:
      f.write("""Testing the work_io module.""")
    finally:
      if hasattr(f, 'close'):
        f.close()

  @classmethod
  def tearDownClass(cls) -> None:
    """
    Tear down the test case.
    """
    cls.clearTempDir()
