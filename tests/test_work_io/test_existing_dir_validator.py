"""
TestExistingDirValidator tests the ExistingDirValidator class from the
'worktoy.work_io' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

import sys

from unittest import TestCase

from tests import WYD
from worktoy.work_io import validateExistingDirectory


class TestExistingDirValidator(TestCase):
  """TestExistingDirValidator tests the existing directory validator."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_dir(self) -> None:
    """Test the existing directory validator."""
    thisFile = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    thisDir = os.path.normpath(os.path.dirname(thisFile))
    validatedDir = validateExistingDirectory(thisDir)
    self.assertEqual(validatedDir, thisDir)

  def test_no_dir(self) -> None:
    """Test the existing directory validator with a non-existing
    directory."""
    here = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    nameSpec = lambda n: os.path.join(here, '__no_dir_%06d.sus' % n)
    c = 0
    while os.path.exists(nameSpec(c)):
      c += 1
      if c > 100:
        raise WYD(RecursionError)
    else:
      with self.assertRaises(FileNotFoundError) as context:
        validateExistingDirectory(nameSpec(c))
      e = context.exception
      self.assertIsInstance(e, FileNotFoundError)
      self.assertIn('No directory exists', str(e))
      #  Non-strict
      self.assertFalse(validateExistingDirectory(nameSpec(c), strict=False))

  def test_is_file(self) -> None:
    """Test the existing directory validator with a file."""
    thisFile = os.path.normpath(os.path.abspath(__file__))
    with self.assertRaises(NotADirectoryError) as context:
      validateExistingDirectory(thisFile)
    e = context.exception
    self.assertIsInstance(e, NotADirectoryError)
    self.assertIn('is not a directory', str(e))
    #  Non-strict
    self.assertFalse(validateExistingDirectory(thisFile, strict=False))
