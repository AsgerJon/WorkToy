"""
TestStochasticWord tests the 'StochasticWord' class from the
'worktoy.examples.lorem_ipsum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os.path
from typing import TYPE_CHECKING

from worktoy.lorem_ipsum import StochasticWord
from . import LoremIpsumTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional

  WeightedFiles: TypeAlias = Optional[tuple[str, float]]


class TestStochasticWord(LoremIpsumTest):
  """
  TestLoremIpsum provides tests for the 'worktoy.examples.lorem_ipsum'
  package.
  """

  @classmethod
  def setUpClass(cls) -> None:
    super().setUpClass()
    cls.dataDir = os.environ.get('WORKTOY_DATA_DIR')

  @classmethod
  def tearDownClass(cls) -> None:
    super().tearDownClass()
    if cls.dataDir is not None:  # pragma: no cover
      os.environ['WORKTOY_DATA_DIR'] = cls.dataDir
    else:  # pragma: no cover
      try:
        del os.environ['WORKTOY_DATA_DIR']
      except KeyError:
        pass

  def setUp(self) -> None:
    super().setUp()
    self.dataDir = os.environ.get('WORKTOY_DATA_DIR')
    self.stochasticWord = StochasticWord()
    self.stochasticWord.realize()  # Preload the data

  def tearDown(self, ) -> None:
    super().tearDown()
    if self.dataDir is not None:  # pragma: no cover
      os.environ['WORKTOY_DATA_DIR'] = self.dataDir
    else:  # pragma: no cover
      try:
        del os.environ['WORKTOY_DATA_DIR']
      except KeyError:
        pass

  def test_realize(self) -> None:
    """
    Test the 'realize' method of the 'StochasticWord' class.
    """
    for _ in range(10):
      word = self.stochasticWord.realize()
      self.assertIsInstance(word, str)

  def test_realize_length(self) -> None:
    """
    Test the 'realizeLength' method of the 'StochasticWord' class.
    """
    for length, words in self.stochasticWord.byLengths.items():
      for _ in range(10):
        word = self.stochasticWord.realizeLength(length)
        self.assertIsInstance(word, str)
        self.assertEqual(len(word), length)

  def test_distribution(self) -> None:
    """
    Test the distribution of the 'StochasticWord' class.
    """
    n = 1000
    predictedMean = self.stochasticWord.meanLen
    predictedVariance = self.stochasticWord.varianceLen
    samples = [len(self.stochasticWord.realize()) for _ in range(n)]
    sampleMean = sum(samples) / n
    sampleVar = sum((x - sampleMean) ** 2 for x in samples) / n
    SE = (predictedVariance / n) ** 0.5
    self.assertLessEqual(abs(sampleMean - predictedMean), 6 * SE)
    SEvar = predictedVariance * (2 / n) ** 0.5
    self.assertLessEqual(abs(sampleVar - predictedVariance), 6 * SEvar)

  def test_recursion_guard(self, ) -> None:
    """
    Testing that the recursion guard of the 'StochasticWord' class works
    correctly.
    """
    setattr(self.stochasticWord, '__data_dir__', None)
    setattr(self.stochasticWord, '__weighted_words__', None)
    setattr(self.stochasticWord, '__min_len__', None)
    setattr(self.stochasticWord, '__max_len__', None)
    setattr(self.stochasticWord, '__by_lengths__', None)
    with self.assertRaises(RecursionError):
      _ = self.stochasticWord._getDataDir(_recursion=True)

    with self.assertRaises(RecursionError):
      _ = self.stochasticWord._getWeightedWords(_recursion=True)

    with self.assertRaises(RecursionError):
      _ = self.stochasticWord._getMinLen(_recursion=True)

    with self.assertRaises(RecursionError):
      _ = self.stochasticWord._getMaxLen(_recursion=True)

    with self.assertRaises(RecursionError):
      _ = self.stochasticWord._getByLengths(_recursion=True)

  def test_index_error_guard(self, ) -> None:
    """
    Testing the index error raised when asking for unavailable lengths.
    """
    with self.assertRaises(IndexError):
      _ = self.stochasticWord.realizeLength(69)

    with self.assertRaises(IndexError):
      _ = self.stochasticWord.realizeLength(420)

  def test_bad_files(self) -> None:
    """
    Testing bad files in a 'StochasticWord' subclass.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    os.environ['WORKTOY_DATA_DIR'] = here

    class Derp(StochasticWord):
      __weighted_files__: WeightedFiles = (
        ('breh.txt', 69.), ('lmao.txt', 420.),
        )

    derp = Derp()
    self.assertIsInstance(derp.dataDir, str)
    self.assertTrue(os.path.isdir(derp.dataDir))
    with self.assertRaises(FileNotFoundError):
      _ = derp.weightedWords

  def test_local_file(self, ) -> None:
    """
    Testing subclass using 'names.txt' in the same directory as the test
    file.
    """
    here = os.path.abspath(os.path.dirname(__file__))

    class Nice(StochasticWord):
      __data_dir__: str = here
      __weighted_files__: WeightedFiles = (
        ('names.txt', 1 / 8),
        ('words.txt', 7 / 8),
        )

    nice = Nice()
    self.assertIsInstance(nice.realize(), str)
    self.assertIsInstance(nice.dataDir, str)
    self.assertTrue(os.path.isdir(nice.dataDir))
    expectedPath = os.path.normpath(here)
    actualPath = os.path.normpath(nice.dataDir)
    self.assertEqual(expectedPath, actualPath)
