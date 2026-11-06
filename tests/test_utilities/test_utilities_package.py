"""
TestUtilitiesPackage tests the public surface of 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import utilities
from worktoy.utilities import combinatorics
from . import UtilitiesTest


class TestUtilitiesPackage(UtilitiesTest):
  """
  The '__all__' of a package is what a star import gives and what the
  package docstring promises. The tests pin that every name listed by
  'worktoy.utilities' and its 'combinatorics' subpackage resolves, and
  that the names the docstrings mention are among them.
  """

  def test_all_names_resolve(self) -> None:
    for name in utilities.__all__:
      with self.subTest(name=name):
        self.assertTrue(hasattr(utilities, name))
    for name in combinatorics.__all__:
      with self.subTest(name=name):
        self.assertTrue(hasattr(combinatorics, name))

  def test_docstring_names_exported(self) -> None:
    for name in utilities.__all__:
      with self.subTest(name=name):
        self.assertIn("'%s'" % name, utilities.__doc__)
    for name in combinatorics.__all__:
      with self.subTest(name=name):
        self.assertIn("'%s'" % name, combinatorics.__doc__)
