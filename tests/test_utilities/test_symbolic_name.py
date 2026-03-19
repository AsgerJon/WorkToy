"""
TestSymbolicName tests the 'SymbolicName' class from the 'worktoy.desc'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import maybe, ExceptionInfo
from worktoy.desc import SymbolicName
from worktoy.waitaminute import TypeException, MissingVariable

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Iterator


class TestSymbolicName(UtilitiesTest):
  """
  TestSymbolicName tests the 'SymbolicName' class from the 'worktoy.desc'
  package.
  """

  def test_init(self, ) -> None:
    """
    This method tests instantiation of 'SymbolicName'.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    for word, part in zip(words, symbolicName.__part_words__):
      self.assertEqual(word, part)

  def test_bool(self, ) -> None:
    """
    Testing the boolean value of 'SymbolicName'. Only empty instances
    without words evaluate 'False'.
    """
    self.assertFalse(SymbolicName(*(), ))
    self.assertTrue(SymbolicName('word', ))

  def test_len(self, ) -> None:
    """
    Testing the length of 'SymbolicName'. The length is determined by the
    number of words in the symbolic name.
    """

    words = 'never', 'gonna', 'give', 'you', 'up'
    for i, word in enumerate(words, ):
      symbolicName = SymbolicName(*words[:i], )
      if not i:
        self.assertFalse(symbolicName)
        continue
      self.assertEqual(len(symbolicName), i)

  def test_iter(self, ) -> None:
    """
    Testing the iteration of 'SymbolicName'. Iterating over a 'SymbolicName'
    instance should yield its words in order.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    for word, part in zip(words, symbolicName):
      self.assertEqual(word, part)

  def test_getitem_index(self, ) -> None:
    """
    Testing the '__getitem__' method on receiving indices.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    for i, word in enumerate(words, ):
      self.assertEqual(symbolicName[i], word)
      self.assertEqual(symbolicName[i - len(words)], word)

  def test_getitem_slice(self, ) -> None:
    """
    Testing the '__getitem__' method on receiving slices.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    for i in range(len(words) + 1):
      for j in range(i, len(words) + 1):
        if i < j:
          self.assertEqual(symbolicName[i:j], words[i:j])

  def test_getitem_bad_type(self, ) -> None:
    """
    Testing the '__getitem__' method on receiving index of unsupported type.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    with self.assertRaises(TypeException) as context:
      _ = symbolicName['lol']
    e = context.exception
    self.assertEqual(e.varName, 'identifier')
    self.assertEqual(e.actualObject, 'lol')
    self.assertIs(e.actualType, str)
    self.assertIn(int, e.expectedTypes)
    self.assertIn(slice, e.expectedTypes)

  def test_getitem_bad_index(self, ) -> None:
    """
    Testing the '__getitem__' method on receiving index out of bounds.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    for index in (69, 420, 1337,):
      with self.assertRaises(IndexError):
        _ = symbolicName[index]

  def test_contains(self, ) -> None:
    """
    Testing if a given word is one of the words in a 'SymbolicName'
    instance using the 'in' operator.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    for word in words:
      self.assertIn(word, symbolicName)
    for word in ('together', 'forever', 'and', 'never_', 'to', 'part'):
      self.assertNotIn(word, symbolicName)

  def test_str_repr(self, ) -> None:
    """
    Testing the string representation of 'SymbolicName'. The string should
    include the class name and the words in the symbolic name.
    """
    self.randomSymbolicName.wordCount = 3
    self.randomSymbolicName.colCount = 10
    for symbolicName in self.randomSymbolicName.row:
      strSpec = """<SymbolicName: %s>"""
      reprSpec = """SymbolicName(%s)"""
      wordsStr = str.join(', ', ["""'%s'""" % w for w in symbolicName.words])
      expectedStr = strSpec % wordsStr
      expectedRepr = reprSpec % wordsStr
      actualStr = str(symbolicName)
      actualRepr = repr(symbolicName)
      self.assertEqual(actualStr, expectedStr)
      self.assertEqual(actualRepr, expectedRepr)

  def test_representations(self, ) -> None:
    """
    Testing the different cases.
    """
    words = 'never', 'gonna', 'give', 'you', 'up'
    symbolicName = SymbolicName(*words, )
    self.assertEqual(symbolicName.snake, 'never_gonna_give_you_up')
    self.assertEqual(symbolicName.pascal, 'NeverGonnaGiveYouUp')
    self.assertEqual(symbolicName.kebab, 'never-gonna-give-you-up')
    self.assertEqual(symbolicName.camel, 'neverGonnaGiveYouUp')

  def test_edge_cases(self, ) -> None:
    """
    Testing edge cases such as empty symbolic names and symbolic names with
    a single word.
    """
    emptySymbolicName = SymbolicName(*(), )
    self.assertFalse(emptySymbolicName)
    self.assertEqual(len(emptySymbolicName), 0)
    self.assertEqual(emptySymbolicName.snake, '')
    self.assertEqual(emptySymbolicName.pascal, '')
    self.assertEqual(emptySymbolicName.kebab, '')
    self.assertEqual(emptySymbolicName.camel, '')

    singleWord = 'hello'
    singleWordSymbolicName = SymbolicName(singleWord, )
    self.assertTrue(singleWordSymbolicName)
    self.assertEqual(len(singleWordSymbolicName), 1)
    self.assertEqual(singleWordSymbolicName.snake, 'hello')
    self.assertEqual(singleWordSymbolicName.pascal, 'Hello')
    self.assertEqual(singleWordSymbolicName.kebab, 'hello')
    self.assertEqual(singleWordSymbolicName.camel, 'hello')

  def test_missing_variable(self) -> None:
    """
    Testing the error raised when somehow '__part_words__' is 'None'.
    """

    symbolicName = SymbolicName('breh')
    object.__setattr__(symbolicName, '__part_words__', None)
    with self.assertRaises(MissingVariable) as context:
      _ = symbolicName.words
    e = context.exception
    self.assertIs(e.instance, symbolicName)
    self.assertEqual(e.varName, 'words')
    self.assertIs(e.type_, tuple)
