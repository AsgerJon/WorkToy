"""
BaseTest provides a common base class for the test classes in the
'test_work_io' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from time import sleep
from unittest import TestCase

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeVar, Callable, Self


class BaseTest(TestCase):
  """
  BaseTest provides a common base class for the test classes in the
  'test_work_io' module.
  """

  @classmethod
  def _createFile(cls, spec: str, index: int) -> Any:
    fileName = spec % index
    filePath = os.path.join(cls.tempDir, fileName)
    f = None
    try:
      f = open(filePath, 'w')
    except Exception as exception:  # pragma: no cover
      raise exception
    else:
      f.write("""This is a temporary file for testing purposes.""")
    finally:
      try:
        f.close()
      except AttributeError:  # pragma: no cover
        pass
    return str(filePath)

  @classmethod
  def _clearFolder(cls, folder: str) -> None:
    """
    Clear the specified folder by removing all files and subdirectories.
    The folder must be absolute.
    """
    for item in os.listdir(folder):
      itemPath = os.path.join(folder, item)
      if os.path.isfile(itemPath) or os.path.islink(itemPath):
        os.remove(itemPath)
        continue
      cls._clearFolder(itemPath)
    os.rmdir(folder)

  @classmethod
  def tearDownClass(cls) -> None:
    cls._clearFolder(cls.testDir)
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  @classmethod
  def setUpClass(cls) -> None:
    cls.here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    cls.testDir = os.path.join(cls.here, '_test_dir')
    cls.tempDir = os.path.join(cls.testDir, 'temp_dir')
    cls.emptyDir = os.path.join(cls.testDir, 'empty_dir')
    os.makedirs(cls.testDir, exist_ok=True)
    os.makedirs(cls.tempDir, exist_ok=True)
    os.makedirs(cls.emptyDir, exist_ok=True)
    cls.emptyPath = os.path.join(cls.testDir, 'empty_path')  # empty
    cls.fileSpec = '_test_%d.tmp'
    cls.tempFiles = [cls._createFile(cls.fileSpec, i) for i in range(10)]
