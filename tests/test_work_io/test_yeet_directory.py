"""
TestYeetDirectory tests the yeetDirectory function from the
'worktoy.work_io' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import WorkIOTest
from worktoy.waitaminute import PathSyntaxException
from worktoy.work_io import yeetDirectory, validateExistingFile
from worktoy.work_io import validateExistingDirectory

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestYeetDirectory(WorkIOTest):
  """
  TestYeetDirectory tests the yeetDirectory function from the
  'worktoy.work_io' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    """
    Cleans up the test environment by removing the temporary directory and
    its contents.
    """
    super().tearDownClass()
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_yeet_temp(self) -> None:
    """
    Tests that yeetDirectory empties the temporary directory.
    """
    self.assertTrue(validateExistingDirectory(self.tempDir))
    for tempFile in self.tempFiles:
      self.assertTrue(validateExistingFile(tempFile))
    yeetDirectory(self.tempDir)
    res = validateExistingDirectory(self.tempDir, strict=False)
    print('derp: %s' % res)
    self.assertFalse(res)
    for tempFile in self.tempFiles:
      with self.assertRaises(FileNotFoundError):
        validateExistingFile(tempFile)

  def test_yeet_non_existent(self) -> None:
    """
    Tests that yeetDirectory raises an error when the directory does not
    exist.
    """
    with self.assertRaises(FileNotFoundError):
      yeetDirectory(self.emptyPath)

  def test_yeet_non_existent_non_strict(self) -> None:
    """
    Tests that yeetDirectory does not raise an error when the directory does
    not exist and strict mode is disabled.
    """
    self.assertFalse(yeetDirectory(self.emptyPath, strict=False))

  def test_yeet_malformed(self) -> None:
    """
    Tests that yeetDirectory raises an error when the path is malformed.
    """
    with self.assertRaises(PathSyntaxException) as context:
      yeetDirectory('imma dir, trust me bro!')
    e = context.exception
    self.assertEqual(repr(e), str(e))

  def test_yeet_nested(self) -> None:
    """
    Tests that yeetDirectory can handle nested directories.
    """
    self.assertTrue(validateExistingDirectory(self.nestedDir))
    yeetDirectory(self.nestedDir)
    with self.assertRaises(FileNotFoundError):
      validateExistingDirectory(self.nestedDir, )
