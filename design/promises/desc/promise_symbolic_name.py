"""
PromiseSymbolicName promises 'SymbolicName' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import SymbolicName


class PromiseSymbolicName(TestCase):
  """
  A 'SymbolicName' keeps a name as its words and writes it in every
  convention: 'snake', 'screamingSnake', 'kebab', 'screamingKebab',
  'pascal' and 'camel'. Each word is capitalized as 'str.capitalize'
  does, so 'HTTPServer' becomes 'Httpserver'. The words are kept as
  given and never split, so 'fontSize' is one word. Two names of the
  same words are equal and hash alike, whatever their case, a name is
  never equal to a string, and a name supports 'len', iteration,
  indexing, which gives a word as given, and 'in' for a word, ignoring
  case. Source:
  the 'SymbolicName' docstring.
  """

  def test_renderings(self) -> None:
    name = SymbolicName('font', 'size')
    self.assertEqual(name.words, ('font', 'size'))
    self.assertEqual(name.snake, 'font_size')
    self.assertEqual(name.screamingSnake, 'FONT_SIZE')
    self.assertEqual(name.kebab, 'font-size')
    self.assertEqual(name.screamingKebab, 'FONT-SIZE')
    self.assertEqual(name.pascal, 'FontSize')
    self.assertEqual(name.camel, 'fontSize')
    self.assertEqual(SymbolicName('HTTPServer').pascal, 'Httpserver')

  def test_equality(self) -> None:
    name = SymbolicName('font', 'size')
    self.assertEqual(SymbolicName('Font', 'SIZE'), name)
    self.assertEqual(hash(SymbolicName('Font', 'SIZE')), hash(name))
    self.assertNotEqual(SymbolicName('size', 'font'), name)

  def test_sequence(self) -> None:
    name = SymbolicName('font', 'size')
    self.assertEqual(len(name), 2)
    self.assertEqual(list(name), ['font', 'size'])
    self.assertEqual(name[1], 'size')
    self.assertEqual(SymbolicName('Font', 'SIZE')[1], 'SIZE')
    self.assertIn('FONT', name)

  def test_words_as_given(self) -> None:
    self.assertEqual(SymbolicName('fontSize').words, ('fontSize',))
    self.assertNotEqual(SymbolicName('font', 'size'), 'font_size')
