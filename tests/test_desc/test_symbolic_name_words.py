"""
TestSymbolicNameWords subclasses 'DescTest' and pins that 'SymbolicName'
refuses a word that is not a string at construction, with
'TypeException' naming it, rather than at the first render. The words
used to be stored unchecked, so 'SymbolicName(1, 2)' built and failed in
the join of its first rendering.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import SymbolicName
from worktoy.waitaminute import TypeException

from . import DescTest


class TestSymbolicNameWords(DescTest):
  """
  TestSymbolicNameWords provides tests for the words of a 'SymbolicName'.
  """

  def test_non_string_refused(self) -> None:
    """An 'int' and a tuple of strings are refused, naming the word."""
    for bad in (1, ('a', 'b'), None, b'x'):
      with self.subTest(bad=bad):
        with self.assertRaises(TypeException) as context:
          SymbolicName('font', bad)
        e = context.exception
        self.assertEqual(e.varName, 'word')
        self.assertIs(e.actualObject, bad)
        self.assertEqual(e.expectedTypes, (str,))

  def test_strings_accepted(self) -> None:
    """Strings, an empty call included, build as before."""
    self.assertEqual(SymbolicName('font', 'size').snake, 'font_size')
    self.assertEqual(SymbolicName().camel, '')
