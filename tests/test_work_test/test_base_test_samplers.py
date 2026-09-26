"""
TestBaseTestSamplers subclasses 'BaseTest' from 'worktoy.work_test' and
pins that every test gets random-data samplers of its own. 'unittest'
builds one instance of a test class per test method, and a sampler held
by that instance lives exactly as long as its test. A test that narrows
'randomInteger' in its 'setUp' therefore leaves every other test with the
default range, whichever class that test belongs to. The same holds for
the 'stochWord' and 'loremSentence' generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticWord, Sentence
from worktoy.work_test import BaseTest
from worktoy.work_test.samplers import IntSampler, FloatSampler
from worktoy.work_test.samplers import GaussianSampler, SymbolicSampler
from worktoy.work_test.samplers import WordSampler, LoremSampler

_GENERATORS = (
  ('randomInteger', IntSampler),
  ('randomFloat', FloatSampler),
  ('randomGaussian', GaussianSampler),
  ('randomSymbolicName', SymbolicSampler),
  ('randomWord', WordSampler),
  ('randomLorem', LoremSampler),
  ('stochWord', StochasticWord),
  ('loremSentence', Sentence),
)


class TestBaseTestSamplers(BaseTest):
  """
  TestBaseTestSamplers provides tests for the ownership of the samplers
  and generators that 'BaseTest' offers every test.
  """

  def _sibling(self) -> BaseTest:
    """The '_sibling' method builds a second instance of this test class
    for the same test method, as 'unittest' does for each test."""
    return type(self)(self._testMethodName)

  def test_generator_types(self) -> None:
    """Each generator is an instance of its documented type."""
    for name, cls in _GENERATORS:
      with self.subTest(name=name):
        self.assertIsInstance(getattr(self, name), cls)

  def test_kept_for_the_whole_test(self) -> None:
    """Within one test, every read returns the same generator, so a
    setting made in 'setUp' is still there in the test method."""
    for name, _ in _GENERATORS:
      with self.subTest(name=name):
        self.assertIs(getattr(self, name), getattr(self, name))
    self.randomInteger.maxVal = 69
    self.assertEqual(self.randomInteger.maxVal, 69)

  def test_own_per_test(self) -> None:
    """Two instances of one test class hold distinct generators."""
    other = self._sibling()
    for name, _ in _GENERATORS:
      with self.subTest(name=name):
        self.assertIsNot(getattr(self, name), getattr(other, name))

  def test_own_per_test_class(self) -> None:
    """Instances of two different test classes hold distinct
    generators."""

    class OtherTest(BaseTest):
      pass

    other = OtherTest()
    for name, _ in _GENERATORS:
      with self.subTest(name=name):
        self.assertIsNot(getattr(self, name), getattr(other, name))

  def test_setting_stays_in_its_test(self) -> None:
    """Narrowing a sampler in one test leaves the sampler of another test
    at its default."""
    other = self._sibling()
    self.randomInteger.maxVal = 7
    self.randomLorem.charCount = 100
    self.assertEqual(other.randomInteger.maxVal, 255)
    self.assertEqual(other.randomLorem.charCount, 40)
