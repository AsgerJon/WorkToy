"""
TestExistingFileValidator tests the functionality of the existing file
validator in the work_io module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

import sys

from unittest import TestCase

from tests import WYD
from worktoy.work_io import validateExistingFile


class TestExistingFileValidator(TestCase):
  """TestExistingFileValidator tests the existing file validator."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_file(self) -> None:
    """Test the existing file validator."""
    thisFile = os.path.normpath(os.path.abspath(__file__))
    validatedFile = validateExistingFile(thisFile)
    self.assertEqual(validatedFile, thisFile)

  def test_no_file(self, ) -> None:
    """Test the existing file validator with a non-existing file."""
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    nameSpec = lambda n: os.path.join(here, '__no_dir_%06d.sus' % n)
    c = 0
    while os.path.exists(nameSpec(c)):
      c += 1
      if c > 100:
        raise WYD(RecursionError)
    else:
      with self.assertRaises(FileNotFoundError) as context:
        validateExistingFile(nameSpec(c))
      e = context.exception
      self.assertIsInstance(e, FileNotFoundError)
      self.assertIn('No file exists at:', str(e))

  def test_no_file_strict(self) -> None:
    """Test the existing file validator with a non-existing file in strict
    mode."""
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    nameSpec = lambda n: os.path.join(here, '__no_dir_%06d.sus' % n)
    c = 0
    while os.path.exists(nameSpec(c)):
      c += 1
      if c > 100:
        raise WYD(RecursionError)
    else:
      validatedFile = validateExistingFile(nameSpec(c), strict=False)
      validatedDir = validateExistingFile(here, strict=False)
      with self.assertRaises(FileNotFoundError) as context:
        validateExistingFile(nameSpec(c), )
      with self.assertRaises(IsADirectoryError) as context:
        validateExistingFile(here)

  def test_is_directory(self) -> None:
    """Test the existing file validator with a directory."""
    with self.assertRaises(IsADirectoryError) as context:
      validateExistingFile(os.path.dirname(__file__))
    e = context.exception
    self.assertIsInstance(e, IsADirectoryError)
    self.assertIn('is not a file', str(e))
