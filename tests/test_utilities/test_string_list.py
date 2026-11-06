"""
TestStringList tests 'stringList' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import stringList
from worktoy.waitaminute import TypeException
from . import UtilitiesTest


class TestStringList(UtilitiesTest):
  """
  'stringList' splits strings on a separator into stripped, non-empty
  pieces, with several separators applied one after another when a
  list or tuple of them is given. The tests pin the docstring examples,
  the stripping and dropping of empty pieces, the sequence of
  separators, and the refusal of any other separator type.
  """

  def test_docstring_examples(self) -> None:
    self.assertEqual(stringList('a, b, c'), ['a', 'b', 'c'])
    self.assertEqual(stringList('a;b,c', separator=[',', ';']),
                     ['a', 'b', 'c'])

  def test_default_separator_is_comma_space(self) -> None:
    self.assertEqual(stringList('a,b, c'), ['a,b', 'c'])

  def test_custom_separator(self) -> None:
    self.assertEqual(stringList('a|b|c', separator='|'), ['a', 'b', 'c'])

  def test_pieces_stripped_and_empty_dropped(self) -> None:
    self.assertEqual(stringList('  a ,, b ,  ', separator=','), ['a', 'b'])
    self.assertEqual(stringList('', separator=','), [])
    self.assertEqual(stringList('   '), [])

  def test_several_arguments(self) -> None:
    self.assertEqual(stringList('a, b', 'c, d'), ['a', 'b', 'c', 'd'])

  def test_no_arguments(self) -> None:
    self.assertEqual(stringList(), [])
    self.assertEqual(stringList(separator=[',', ';']), [])

  def test_tuple_of_separators(self) -> None:
    self.assertEqual(stringList('a;b|c', separator=(';', '|')),
                     ['a', 'b', 'c'])

  def test_separators_apply_in_order(self) -> None:
    #  Splitting on 'ab' before 'b' leaves no 'b' for the second pass,
    #  while the other order does.
    self.assertEqual(stringList('xaby', separator=['ab', 'b']), ['x', 'y'])
    self.assertEqual(stringList('xaby', separator=['b', 'ab']), ['xa', 'y'])

  def test_bad_separator_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      stringList('a, b', separator=42)
    self.assertEqual(context.exception.varName, 'separator')
    self.assertEqual(context.exception.actualObject, 42)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str, list, tuple))
    self.assertIn("'separator'", str(context.exception))
    self.assertIn("'str', 'list' or 'tuple'", str(context.exception))
