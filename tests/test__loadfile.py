#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
import os
from typing import NoReturn
import unittest
import tempfile
from unittest.mock import patch

from worktoy.core import maybe
from worktoy.waitaminute import DIOError
from worktoy.dio import loadFile


class LoadFileTestCase(unittest.TestCase):
  """Testing loadFile"""

  _recursionFlagAssign = False
  _recursionFlagExists = False

  @classmethod
  def _getTempPath(cls) -> str:
    """Getter-function for temporary path"""
    if cls._tempPath is None:
      if cls._recursionFlagAssign:
        raise RecursionError
      cls._recursionFlagAssign = True
      cls._assignTempPath()
      return cls._getTempPath()
    cls._recursionFlagAssign = False
    if cls._tempPathExists():
      cls._recursionFlagExists = False
      return cls._tempPath
    if cls._recursionFlagExists:
      raise RecursionError
    cls._recursionFlagExists = True
    cls._createTempPath()
    return cls._getTempPath()

  @classmethod
  def _assignTempPath(cls) -> NoReturn:
    """Assigns the temporary path variable. This points to the _temp
    directory in the dir specified by the worktoy environment variable."""
    here = os.getcwd()
    root = maybe(os.getenv('WORKTOYPATH'), here)
    cls._tempPath = os.path.join(root, '_tempDir')

  @classmethod
  def _tempPathExists(cls) -> bool:
    """Checks if temporary path exists"""
    tempPath = cls._getTempPath()
    if tempPath is None:
      return False
    if os.path.isfile(tempPath):
      raise NotADirectoryError
    if os.path.isdir(tempPath):
      return True
    return False

  @classmethod
  def _createTempPath(cls) -> bool:
    """Creates the temporary path if it does not already exist."""
    tempPath = cls._getTempPath()
    if tempPath is None:
      return False
    if os.path.isfile(tempPath):
      raise NotADirectoryError
    if os.path.isdir(tempPath):
      return True
    os.makedirs(tempPath)
    return cls._createTempPath()

  _tempPath = None
  tempDir = None
  file_path = None

  @classmethod
  def setUpClass(cls) -> NoReturn:
    """Sets up the class"""
    cls.tempDir = tempfile.TemporaryDirectory()
    cls.file_path = os.path.join(cls.tempDir.name, 'test.txt')
    cls.non_existing_file_path = os.path.join(
      cls.tempDir.name, 'non_existing_file.txt')
    cls.no_access_file_path = os.path.join(
      cls.tempDir.name, 'no_access_file.txt')
    cls.directory_path = os.path.join(
      cls.tempDir.name, 'directory_path/')
    cls.file_with_decoding_error_path = os.path.join(
      cls.tempDir.name, 'file_with_decoding_error.txt')
    cls.file_with_io_error_path = os.path.join(
      cls.tempDir.name, 'file_with_io_error.txt')
    cls.unknown_error_file_path = os.path.join(
      cls.tempDir.name, 'unknown_error_file.txt')

    # Create an existing file
    with open(cls.file_path, 'w') as file:
      file.write('This is a test file.')

  @classmethod
  def tearDownClass(cls) -> NoReturn:
    """Tears down class"""
    cls.tempDir.cleanup()
