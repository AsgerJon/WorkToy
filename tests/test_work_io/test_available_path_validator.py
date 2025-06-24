"""
TestAvailablePathValidator tests the AvailablePathValidator class from the
'worktoy.work_io' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

import sys

from unittest import TestCase

from tests import WYD
from worktoy.waitaminute import PathSyntaxException
from worktoy.work_io import validateAvailablePath


class TestAvailablePathValidator(TestCase):
  """TestAvailablePathValidator tests the available path validator."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_empty_path(self) -> None:
    """Test the available path validator with an empty path."""
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    nameSpec = lambda n: os.path.join(here, '__no_dir_%06d.sus' % n)
    c = 0
    while os.path.exists(nameSpec(c)):
      c += 1
      if c > 100:
        raise WYD(RecursionError)
    else:
      emptyPath = nameSpec(c)
      res = validateAvailablePath(emptyPath)
      self.assertEqual(res, emptyPath)

  def test_file_path(self) -> None:
    """Test the available path validator with a file path."""
    thisFile = os.path.normpath(os.path.abspath(__file__))
    with self.assertRaises(FileExistsError) as context:
      validateAvailablePath(thisFile)
    e = context.exception
    self.assertIsInstance(e, FileExistsError)
    self.assertIn('already exists', str(e))

  def test_directory_path(self) -> None:
    """Test the available path validator with a directory path."""
    thisDir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    with self.assertRaises(FileExistsError) as context:
      validateAvailablePath(thisDir)
    e = context.exception
    self.assertIsInstance(e, FileExistsError)
    self.assertIn('already exists', str(e))

  def test_malformed_path(self) -> None:
    """Test the available path validator with a malformed path."""
    malformedPath = 'imma a path, trust!'
    with self.assertRaises(PathSyntaxException) as context:
      validateAvailablePath(malformedPath)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.badPath, malformedPath)
