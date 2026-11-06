"""
TestBaseSampler tests 'BaseSampler' from 'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import Random

from worktoy.desc import AttriBox, Alias, Field
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import BaseSampler, IntSampler
from worktoy.work_test.samplers import WordSampler, LOREM_WORDS
from . import WorkTestTest, Cheat, Renamed


class TestBaseSampler(WorkTestTest):
  """
  'BaseSampler' is what every sampler shares: the two counts with their
  aliases and keywords, the keyword constructor over the synonyms of
  '__key_groups__' merged along the resolution order, a generator and a
  seed of its own, and the item, row and table drawn through the two
  hooks with every value checked against the value type. The tests pin
  the merge of the key groups through 'Renamed', every synonym, the
  refusals of an unknown keyword, a count below one, a count or a seed
  of the wrong type and a value of the wrong type through 'Cheat', the
  shapes, the call, the iteration, the seeding, and the two texts, on
  'WordSampler', the sampler with no setting of its own.
  """

  def test_settings_are_boxes_and_aliases(self) -> None:
    for name in ('colCount', 'rowCount', 'random'):
      with self.subTest(name=name):
        self.assertIsInstance(BaseSampler.__dict__[name], AttriBox)
    for name in ('width', 'height', 'size', 'count'):
      with self.subTest(name=name):
        self.assertIsInstance(BaseSampler.__dict__[name], Alias)
    for name in ('seed', 'valueType', 'item', 'row', 'table'):
      with self.subTest(name=name):
        self.assertIsInstance(BaseSampler.__dict__[name], Field)

  def test_key_groups_merge_along_the_order(self) -> None:
    groups = IntSampler._getKeyGroups()
    self.assertEqual([*groups],
                     ['minVal', 'maxVal', 'colCount', 'rowCount', 'seed'])
    self.assertEqual(groups['colCount'], ('colCount', 'width', 'size'))
    self.assertEqual(groups['rowCount'], ('rowCount', 'height', 'count'))
    self.assertEqual(groups['seed'], ('seed', 'randomSeed'))
    self.assertEqual([*WordSampler._getKeyGroups()],
                     ['colCount', 'rowCount', 'seed'])
    renamed = Renamed._getKeyGroups()
    self.assertEqual([*renamed],
                     ['colCount', 'minVal', 'maxVal', 'rowCount', 'seed'])
    self.assertEqual(renamed['colCount'], ('cols',))
    self.assertEqual(renamed['minVal'], groups['minVal'])
    self.assertEqual(Renamed(cols=2).colCount, 2)
    self.assertEqual(Renamed(cols=2, min=3).minVal, 3)
    with self.assertRaises(TypeError) as context:
      Renamed(width=2)
    self.assertEqual(str(context.exception),
                     "Renamed() got an unexpected keyword argument 'width'")

  def test_keyword_synonyms(self) -> None:
    for key in ('colCount', 'width', 'size'):
      with self.subTest(key=key):
        self.assertEqual(WordSampler(**{key: 3}).colCount, 3)
    for key in ('rowCount', 'height', 'count'):
      with self.subTest(key=key):
        self.assertEqual(WordSampler(**{key: 2}).rowCount, 2)
    for key in ('seed', 'randomSeed'):
      with self.subTest(key=key):
        self.assertEqual(WordSampler(**{key: 9}).seed, 9)
    sampler = WordSampler(width=2, size=5, height=3, count=4)
    self.assertEqual((sampler.colCount, sampler.rowCount), (2, 3))

  def test_unknown_keyword_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      WordSampler(foo=1)
    self.assertEqual(str(context.exception), "WordSampler() got an "
                                             "unexpected keyword argument "
                                             "'foo'")
    with self.assertRaises(TypeError) as context:
      WordSampler(size=2, wordCount=3)
    self.assertEqual(str(context.exception), "WordSampler() got an "
                                             "unexpected keyword argument "
                                             "'wordCount'")
    with self.assertRaises(DispatchException) as context:
      WordSampler(3)
    self.assertIs(context.exception.dispatch,
                  WordSampler.__dict__['__init__'])
    self.assertIsNot(context.exception.dispatch,
                     BaseSampler.__dict__['__init__'])
    self.assertEqual(context.exception.posArgs, (3,))
    self.assertEqual(context.exception.keyArgs, {})
    self.assertIn("no overload of 'WordSampler.__init__' accepts",
                  str(context.exception))
    self.assertIn('<int 3>', str(context.exception))

  def test_counts(self) -> None:
    sampler = WordSampler()
    self.assertEqual((sampler.colCount, sampler.rowCount), (1, 1))
    sampler.width = 3
    sampler.height = 2
    self.assertEqual((sampler.colCount, sampler.rowCount), (3, 2))
    self.assertEqual((sampler.size, sampler.count), (3, 2))
    sampler.colCount = 4.0
    self.assertEqual(sampler.colCount, 4)
    self.assertIs(type(sampler.colCount), int)
    for value in (0, -1, 0.5):
      with self.subTest(value=value):
        with self.assertRaises(ValueError) as context:
          sampler.colCount = value
        self.assertEqual(str(context.exception),
                         'Column count must be a positive integer.')
        with self.assertRaises(ValueError) as context:
          sampler.rowCount = value
        self.assertEqual(str(context.exception),
                         'Row count must be a positive integer.')
    with self.assertRaises(TypeException) as context:
      sampler.colCount = '3'
    self.assertTypeRefused(context.exception, 'colCount', '3', int)
    with self.assertRaises(TypeException) as context:
      WordSampler(rowCount='2')
    self.assertTypeRefused(context.exception, 'rowCount', '2', int)
    with self.assertRaises(ValueError) as context:
      WordSampler(count=0)
    self.assertEqual(str(context.exception),
                     'Row count must be a positive integer.')
    self.assertEqual((sampler.colCount, sampler.rowCount), (4, 2))
    sampler.colCount = 1
    sampler.rowCount = 1
    self.assertEqual((sampler.colCount, sampler.rowCount), (1, 1))
    one = WordSampler(size=1, count=1)
    self.assertEqual((one.colCount, one.rowCount), (1, 1))
    long = WordSampler(count=300, seed=1)
    self.assertEqual(len(long.table), 300)
    self.assertEqual(len([*long]), 300)

  def test_seed(self) -> None:
    sampler = WordSampler()
    self.assertIsNone(sampler.seed)
    self.assertIsInstance(sampler.random, Random)
    self.assertIsNot(sampler.random, WordSampler().random)
    sampler.seed = 4
    self.assertEqual(sampler.seed, 4)
    first = [sampler() for _ in range(6)]
    sampler.seed = 4
    self.assertEqual([sampler() for _ in range(6)], first)
    self.assertEqual([WordSampler(seed=4)() for _ in range(1)], first[:1])
    other = WordSampler(seed=4)
    _ = [WordSampler() for _ in range(3)]
    self.assertEqual([other() for _ in range(6)], first)
    with self.assertRaises(TypeException) as context:
      sampler.seed = 'x'
    self.assertTypeRefused(context.exception, 'seed', 'x', int)
    with self.assertRaises(TypeException) as context:
      WordSampler(randomSeed=2.5)
    self.assertTypeRefused(context.exception, 'seed', 2.5, int)
    self.assertEqual(sampler.seed, 4)
    self.assertIs(WordSampler(seed=True).seed, True)

  def test_shapes(self) -> None:
    sampler = WordSampler(width=3, height=2, seed=1)
    self.assertIs(sampler.valueType, str)
    self.assertIsInstance(sampler.item, str)
    self.assertIn(sampler(), LOREM_WORDS)
    row = sampler.row
    self.assertIsInstance(row, tuple)
    self.assertEqual(len(row), 3)
    for word in row:
      self.assertIn(word, LOREM_WORDS)
    table = sampler.table
    self.assertEqual(len(table), 2)
    for line in table:
      self.assertEqual(len(line), 3)
    rows = [*sampler]
    self.assertEqual(len(rows), 2)
    for line in rows:
      self.assertEqual(len(line), 3)
    self.assertIsNot(sampler.row, sampler.row)

  def test_value_of_wrong_type_refused(self) -> None:
    cheat = Cheat(seed=1)
    self.assertIs(cheat.valueType, int)
    self.assertIsInstance(cheat(), str)
    with self.assertRaises(TypeException) as context:
      _ = cheat.row
    self.assertEqual(context.exception.varName, 'value')
    self.assertIsInstance(context.exception.actualObject, str)
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'value' to be an instance of 'int'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      _ = cheat.table
    self.assertEqual(context.exception.varName, 'value')

  def test_texts(self) -> None:
    self.assertEqual(str(WordSampler()), "<WordSampler: 'str' (1, 1)>")
    self.assertEqual(str(WordSampler(size=3, count=2)),
                     "<WordSampler: 'str' (3, 2)>")
    self.assertEqual(repr(WordSampler()),
                     'WordSampler(colCount=1, rowCount=1, seed=None)')
    self.assertEqual(repr(WordSampler(size=3, count=2, seed=7)),
                     'WordSampler(colCount=3, rowCount=2, seed=7)')
    self.assertEqual(repr(Renamed(cols=2)), 'Renamed(colCount=2, minVal=0, '
                                            'maxVal=255, rowCount=1, '
                                            'seed=None)')

  def test_random_shapes(self) -> None:
    self.randomInteger = IntSampler(1, 6, seed=self.__sampler_seed__)
    self.randomInteger.size = 6
    for width, height in zip(self.randomInteger.row, self.randomInteger.row):
      with self.subTest(width=width, height=height):
        sampler = WordSampler(width=width, height=height, seed=width)
        self.assertEqual(len(sampler.row), width)
        self.assertEqual(len(sampler.table), height)
        self.assertEqual(len([*sampler]), height)
