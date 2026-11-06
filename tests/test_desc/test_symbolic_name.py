"""
TestSymbolicName tests 'SymbolicName' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import SymbolicName
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import ReadOnlyError
from . import DescTest


class TestSymbolicName(DescTest):
  """
  One name must be written in several conventions from one set of
  words, and two names of the same words must count as one whatever
  their case. The tests pin the six renderings, the empty and the
  single-word name, equality and hash ignoring case, membership,
  indexing and slicing with their refusals, the texts, the constructor,
  and the name as a read-only class variable.
  """

  def test_renderings(self) -> None:
    name = SymbolicName('font', 'Size', 'PX')
    self.assertEqual(name.words, ('font', 'Size', 'PX'))
    self.assertEqual(name.snake, 'font_size_px')
    self.assertEqual(name.screamingSnake, 'FONT_SIZE_PX')
    self.assertEqual(name.kebab, 'font-size-px')
    self.assertEqual(name.screamingKebab, 'FONT-SIZE-PX')
    self.assertEqual(name.pascal, 'FontSizePx')
    self.assertEqual(name.camel, 'fontSizePx')

  def test_short_names(self) -> None:
    empty = SymbolicName()
    self.assertEqual((empty.camel, empty.pascal, empty.snake), ('', '', ''))
    self.assertFalse(empty)
    self.assertEqual(len(empty), 0)
    single = SymbolicName('Word')
    self.assertEqual(single.camel, 'word')
    self.assertEqual(single.pascal, 'Word')
    self.assertTrue(single)
    self.assertEqual(len(single), 1)

  def test_equality_ignores_case(self) -> None:
    self.assertEqual(SymbolicName('a', 'B'), SymbolicName('A', 'b'))
    self.assertNotEqual(SymbolicName('a', 'b'), SymbolicName('b', 'a'))
    self.assertNotEqual(SymbolicName('a'), SymbolicName('a', 'b'))
    self.assertEqual(hash(SymbolicName('a', 'B')),
                     hash(SymbolicName('A', 'b')))
    self.assertEqual(len({SymbolicName('a'), SymbolicName('A')}), 1)
    self.assertIs(SymbolicName('a').__eq__('a'), NotImplemented)
    self.assertFalse(SymbolicName('a') == 'a')

  def test_membership(self) -> None:
    name = SymbolicName('font', 'Size')
    self.assertIn('size', name)
    self.assertIn('FONT', name)
    self.assertNotIn('px', name)
    self.assertNotIn(5, name)

  def test_indexing_and_slicing(self) -> None:
    name = SymbolicName('a', 'b', 'c')
    self.assertEqual(name[0], 'a')
    self.assertEqual(name[-1], 'c')
    self.assertEqual(name[1:], ('b', 'c'))
    self.assertEqual([*name], ['a', 'b', 'c'])
    with self.assertRaises(IndexError) as context:
      _ = name[3]
    self.assertEqual(str(context.exception), '3')
    with self.assertRaises(IndexError) as context:
      _ = name[-4]
    self.assertEqual(str(context.exception), '-1')
    with self.assertRaises(TypeException) as context:
      _ = name['a']
    self.assertEqual(context.exception.varName, 'identifier')
    self.assertEqual(context.exception.actualObject, 'a')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int, slice))
    self.assertIn("'identifier'", str(context.exception))
    self.assertIn("'int' or 'slice'", str(context.exception))

  def test_text(self) -> None:
    name = SymbolicName('a', 'b')
    self.assertEqual(str(name), "<SymbolicName: 'a', 'b'>")
    self.assertEqual(repr(name), "SymbolicName('a', 'b')")
    self.assertEqual(repr(SymbolicName()), 'SymbolicName()')

  def test_constructor(self) -> None:
    with self.assertRaises(TypeException) as context:
      SymbolicName('a', 5)
    self.assertEqual(context.exception.varName, 'word')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'word'", str(context.exception))
    blank = SymbolicName.__new__(SymbolicName)
    with self.assertRaises(MissingVariable) as context:
      _ = blank.words
    self.assertEqual(context.exception.varName, 'words')
    self.assertIs(context.exception.instance, blank)
    self.assertEqual(context.exception.expectedTypes, (tuple,))
    self.assertEqual(str(context.exception),
                     "Missing 'SymbolicName.words: tuple'!")

  def test_read_only_class_variable(self) -> None:
    class Owner:
      name = SymbolicName('font', 'size')

    owner = Owner()
    self.assertIs(owner.name, Owner.__dict__['name'])
    with self.assertRaises(ReadOnlyError) as context:
      owner.name = SymbolicName('x')
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, Owner.__dict__['name'])
    self.assertEqual(context.exception.newVal, SymbolicName('x'))
    self.assertIn("'Owner.name'", str(context.exception))

  def test_random_names(self) -> None:
    for name in self.randomSymbolicName.row:
      with self.subTest(name=name.snake):
        self.assertEqual(name.snake, '_'.join(name.words).lower())
        self.assertEqual(name.kebab.replace('-', '_'), name.snake)
        self.assertEqual(name.screamingSnake, name.snake.upper())
        self.assertEqual(name.pascal[0], name.camel[0].upper())
        self.assertEqual(SymbolicName(*name.words), name)

  def test_positive_indices_and_reverse_inequality(self) -> None:
    name = SymbolicName('a', 'b', 'c')
    self.assertEqual(name[1], 'b')
    self.assertEqual(name[2], 'c')
    self.assertEqual(name[-2], 'b')
    self.assertNotEqual(SymbolicName('b', 'a'), SymbolicName('a', 'b'))
    self.assertNotEqual(SymbolicName('a', 'b'), SymbolicName('a'))
