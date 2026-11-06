"""
TestSymbolicSampler tests 'SymbolicSampler' from
'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import SymbolicName
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import SymbolicSampler, LOREM_WORDS
from . import WorkTestTest


class TestSymbolicSampler(WorkTestTest):
  """
  'SymbolicSampler' draws names made of real words, 'wordCount' of them,
  three unless set otherwise and never fewer than one. The tests pin
  the defaults, the count by position and by every synonym, the
  refusals, the names drawn, and the repeat of a seeded sampler.
  """

  def test_defaults(self) -> None:
    sampler = SymbolicSampler()
    self.assertEqual(sampler.wordCount, 3)
    self.assertIs(sampler.valueType, SymbolicName)
    self.assertEqual(repr(sampler), 'SymbolicSampler(wordCount=3, '
                                    'colCount=1, rowCount=1, seed=None)')
    self.assertEqual(str(sampler),
                     "<SymbolicSampler: 'SymbolicName' (1, 1)>")

  def test_word_count(self) -> None:
    self.assertEqual(SymbolicSampler(2).wordCount, 2)
    self.assertEqual(SymbolicSampler(2, seed=1).seed, 1)
    for key in ('wordCount', 'numWords', 'num_words', 'word_count'):
      with self.subTest(key=key):
        self.assertEqual(SymbolicSampler(**{key: 4}).wordCount, 4)
    self.assertEqual(SymbolicSampler(wordCount=5.0).wordCount, 5)
    sampler = SymbolicSampler()
    sampler.wordCount = 1
    self.assertEqual(len([*sampler()]), 1)

  def test_refusals(self) -> None:
    for value in (0, -1, 0.5):
      with self.subTest(value=value):
        with self.assertRaises(ValueError) as context:
          SymbolicSampler(wordCount=value)
        self.assertEqual(str(context.exception),
                         'Word count must be a positive integer.')
    with self.assertRaises(TypeException) as context:
      SymbolicSampler(wordCount='x')
    self.assertTypeRefused(context.exception, 'wordCount', 'x', int)
    with self.assertRaises(DispatchException) as context:
      SymbolicSampler('x')
    self.assertIs(context.exception.dispatch,
                  SymbolicSampler.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, ('x',))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("no overload of 'SymbolicSampler.__init__' accepts",
                  str(context.exception))

  def test_names(self) -> None:
    sampler = SymbolicSampler(2, seed=1, size=5)
    for name in sampler.row:
      with self.subTest(name=str(name)):
        self.assertIsInstance(name, SymbolicName)
        words = [*name]
        self.assertEqual(len(words), 2)
        for word in words:
          self.assertIn(word, LOREM_WORDS)
    first = [str(name) for name in SymbolicSampler(3, seed=4).row]
    second = [str(name) for name in SymbolicSampler(3, seed=4).row]
    self.assertEqual(first, second)
    self.assertEqual(str(SymbolicSampler(2, seed=1)()),
                     "<SymbolicName: 'enim', 'eum'>")

  def test_random_names(self) -> None:
    self.randomSymbolicName.size = 6
    for name in self.randomSymbolicName.row:
      with self.subTest(name=str(name)):
        self.assertEqual(len([*name]), 3)
    self.assertEqual(self.randomSymbolicName.seed, self.__sampler_seed__)
