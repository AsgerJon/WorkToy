"""
TestSymbolicNameContains subclasses 'DescTest' and pins that 'in' on a
'SymbolicName' ignores case, as its equality and hash do.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import SymbolicName

from . import DescTest


class TestSymbolicNameContains(DescTest):
  """
  TestSymbolicNameContains provides tests for 'in' on a 'SymbolicName'.
  """

  def test_case_ignored(self) -> None:
    """This method tests that a word differing only in case is not
    missing from a name equal to one holding it. 'Font' is in
    'SymbolicName("font", "size")'."""
    name = SymbolicName('font', 'size')
    self.assertEqual(name, SymbolicName('Font', 'Size'))
    self.assertIn('Font', name)
    self.assertIn('SIZE', name)
    self.assertNotIn('color', name)

  def test_non_text_not_contained(self) -> None:
    """This method tests that something other than a 'str' does not
    raise. It is in no name."""
    name = SymbolicName('font', 'size')
    self.assertNotIn(5, name)
    self.assertNotIn(None, name)
