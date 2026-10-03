"""
TestSamplerKeywords subclasses 'SamplerTest' and pins the keywords a
sampler takes. A float sampler takes an 'int' bound, since an 'int' casts
to a 'float' without loss; it used to refuse 'FloatSampler(minVal=0,
maxVal=1)' with 'TypeException'. A keyword naming no setting raises the
'TypeError' Python raises for an unexpected keyword argument; a
misspelled one such as 'IntSampler(mni=3)' used to be dropped without a
word.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import IntSampler, FloatSampler
from worktoy.work_test.samplers import GaussianSampler, SymbolicSampler
from worktoy.waitaminute import TypeException

from . import SamplerTest


class TestSamplerKeywords(SamplerTest):
  """
  TestSamplerKeywords provides tests for the keywords of the samplers.
  """

  def test_float_takes_int(self) -> None:
    """A float sampler takes 'int' bounds as floats."""
    sampler = FloatSampler(minVal=0, maxVal=2)
    self.assertEqual((sampler.minVal, sampler.maxVal), (0.0, 2.0))
    self.assertIs(type(sampler.minVal), float)
    gaussian = GaussianSampler(mean=1, stdDev=2)
    self.assertEqual((gaussian.mean, gaussian.stdDev), (1.0, 2.0))

  def test_lossy_value_refused(self) -> None:
    """A value that does not cast without loss is still refused."""
    with self.assertRaises(TypeException):
      IntSampler(minVal=2.5)
    with self.assertRaises(TypeException):
      FloatSampler(minVal='low')

  def test_unknown_keyword_refused(self) -> None:
    """A keyword naming no setting raises 'TypeError' naming it."""
    for factory in (IntSampler, FloatSampler, GaussianSampler,
                    SymbolicSampler):
      with self.subTest(factory=factory.__name__):
        with self.assertRaises(TypeError) as context:
          factory(mni=3)
        self.assertIn("'mni'", str(context.exception))

  def test_synonyms_accepted(self) -> None:
    """The synonyms of a setting are accepted."""
    self.assertEqual(IntSampler(minimum=3, maximum=9).minVal, 3)
    self.assertEqual(SymbolicSampler(count=4).wordCount, 4)
