"""
TestIndex subclasses 'MarkworkTest' and provides tests for the 'Index'
class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from worktoy.markwork import Index
from worktoy.utilities import ExceptionInfo, textFmt
from . import MarkworkTest
from .examples import ReadmeExample

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class TestIndex(MarkworkTest):
  """
  TestIndex subclasses 'MarkworkTest' and provides tests for the 'Index'
  class in the 'worktoy.markwork' package.
  """

  def setUp(self, ) -> None:
    """
    This method sets up the test by creating an instance of 'Index' and
    assigning it to 'self.index'.
    """
    super().setUp()
    self.index = ReadmeExample()

  def test_readme_example(self, ) -> None:
    """
    This method retrieves the 'Markdown' content of the 'ReadmeExample'
    class from the tests.test_markwork.examples._readme_example module.
    """
    content = self.index.markdown()
    self.assertIsInstance(content, str)

  def test_fallback_dir(self) -> None:
    """
    This method covers the case where an 'Index' subclass has a fallback
    directory.
    """

    class Foo(Index):
      __fallback_dir__ = os.path.dirname(__file__)

    self.assertTrue(os.path.exists(Foo().fileDir()))

  def test_no_fallback_dir(self) -> None:
    """
    This method covers the case where an 'Index' subclass is missing a
    fallback directory.
    """

    class Foo(Index):
      __fallback_dir__ = None

    self.assertTrue(os.path.exists(Foo().fileDir()))

  def test_env_var_dir(self, ) -> None:
    """
    This method tests the case where an 'Index' subclass uses an
    environment variable to determine the directory of the file.
    """

    class Foo(Index):
      __dir_env_var__ = self.dirEnvVar

    foo = Foo()
    self.assertTrue(os.path.exists(foo.fileDir()))

  def test_bad_index(self, ) -> None:
    """
    This method covers 'Index' subclasses missing various components.
    """
    self.randomSymbolicName.wordCount = 3
    here = os.path.abspath(os.path.dirname(__file__))
    dirEnvVar = (*os.environ.keys(), 'breh')[0]
    while dirEnvVar in os.environ:
      dirEnvVar = self.randomSymbolicName.item.screamingSnake
    with self.assertRaises(NotADirectoryError):
      class Sus(Index):
        __dir_env_var__ = dirEnvVar
        __fallback_dir__ = os.path.abspath(__file__)
        __base_name__ = os.path.basename(__file__)

      sus = Sus()
      _ = sus.fileDir()

    res = None
    with self.assertRaises(FileNotFoundError):
      class Sus(Index):
        __dir_env_var__ = dirEnvVar
        __fallback_dir__ = os.path.join(here, 'trolololo')
        __base_name__ = os.path.basename(__file__)

      sus = Sus()
      res = sus.fileDir()

  def test_save(self, ) -> None:
    """
    This method tests the 'save' method.
    """

    class Readme(ReadmeExample):
      """
      Subclass of 'ReadmeExample' with directory at the temporary
      directory provided by the 'tempfile' module.
      """
      __fallback_dir__ = self._getTempDir()

    readme = Readme()
    filePath = readme.save()
    self.assertTrue(os.path.exists(filePath))

    readme.baseName = str.replace("""never gonna give you up""", ' ', '_')
    filePath2 = readme.save()
    self.assertTrue(os.path.exists(filePath2))

    filePath3 = os.path.join(
      self._getTempDir(),
      'never_gonna_let_you_down.md',
      )

    filePath3b = readme.save(filePath3)
    self.assertTrue(os.path.exists(filePath3b))
    self.assertEqual(filePath3, filePath3b)
