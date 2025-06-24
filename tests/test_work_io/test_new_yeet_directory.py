"""
TestNewYeetDirectory tests the newDirectory and yeetDirectory functions
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from unittest import TestCase
from typing import TYPE_CHECKING

from tests import WYD
from worktoy.work_io import validateExistingDirectory, yeetDirectory
from worktoy.work_io import newDirectory, validateAvailablePath

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestNewYeetDirectory(TestCase):
  """TestNewYeetDirectory tests the newDirectory and yeetDirectory
  functions."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_new_yeet_directory(self) -> None:
    """
    newDirectory creates a new directory, and yeetDirectory removes it.
    """
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    nameSpec = lambda n: os.path.join(here, '__new_dir_%06d.sus' % n)
    c = 0
    while os.path.exists(nameSpec(c)):
      c += 1
      if c > 100:
        raise WYD(RecursionError)
    else:
      freePath = validateAvailablePath(nameSpec(c))
      newDir = newDirectory(freePath)
      dirPath = validateExistingDirectory(newDir)
      yeetDirectory(newDir)
      validateAvailablePath(dirPath)

  def test_yeet_non_existing_directory(self) -> None:
    """
    yeetDirectory raises FileNotFoundError if the directory does not exist.
    """
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    nameSpec = lambda n: os.path.join(here, '__no_dir_%06d.sus' % n)
    c = 0
    while os.path.exists(nameSpec(c)):
      c += 1
      if c > 100:
        raise WYD(RecursionError)
    else:
      with self.assertRaises(FileNotFoundError) as context:
        yeetDirectory(nameSpec(c))
      e = context.exception
      self.assertIsInstance(e, FileNotFoundError)
      self.assertIn('No directory exists at:', str(e))
    self.assertIsNone(yeetDirectory(nameSpec(c), strict=False))

  def test_yeet_file(self) -> None:
    """
    yeetDirectory raises NotADirectoryError if the path is a file.
    """
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    there = os.path.join(here, '__yeet_file.sus')
    f = None
    try:
      f = open(there, 'w')
    except Exception as e:
      raise e
    else:
      f.close()
      with self.assertRaises(NotADirectoryError) as context:
        yeetDirectory(there)
      e = context.exception
      self.assertIsInstance(e, NotADirectoryError)
      self.assertIn('is not a directory', str(e))
    finally:
      if hasattr(f, 'close'):
        f.close()

  def test_yeet_nested(self) -> None:
    """
    Tests yeeting nested folder
    """
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    there = os.path.join(here, 'never', 'gonna', 'give', 'you', 'up')
    os.makedirs(there, exist_ok=True)
    yeetDirectory(there)
    self.assertFalse(os.path.exists(there), )
