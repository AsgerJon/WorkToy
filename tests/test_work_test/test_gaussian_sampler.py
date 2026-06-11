"""
TestGaussianSampler subclasses 'SamplerTest' and provides testing of the
'GaussianSampler' class from the 'worktoy.work_test.samplers' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import TypeCastException
from worktoy.work_test.samplers import GaussianSampler
from . import SamplerTest


class TestGaussianSampler(SamplerTest):
  """
  TestGaussianSampler subclasses 'SamplerTest' and provides testing of the
  'GaussianSampler' class from the 'worktoy.work_test.samplers' package.
  """

  def test_init(self, ) -> None:
    """
    This method tests the initialization of the 'GaussianSampler' class,
    which provides the following constructor overloads:

    @overload(float, float)
    def __init__(self, mean: float, stdDev: float, **kw) -> None: ...

    @overload(float, )
    def __init__(self, mean: float, **kw) -> None: ...

    @overload()
    def __init__(self, **kw) -> None: ...
    """

    floatFloatKwarg = GaussianSampler(69., 420., lmao=True)
    self.assertEqual(floatFloatKwarg.mean, 69.)
    self.assertEqual(floatFloatKwarg.stdDev, 420.)
    floatFloatSampler = GaussianSampler(69., 420.)
    self.assertEqual(floatFloatSampler.mean, 69.)
    self.assertEqual(floatFloatSampler.stdDev, 420.)
    floatKwarg = GaussianSampler(69., breh=False)
    self.assertEqual(floatKwarg.mean, 69.)
    self.assertEqual(floatKwarg.stdDev, 1.)
    floatSampler = GaussianSampler(69.)
    self.assertEqual(floatSampler.mean, 69.)
    self.assertEqual(floatSampler.stdDev, 1.)
    defaultSampler = GaussianSampler()
    self.assertEqual(defaultSampler.mean, 0.)
    self.assertEqual(defaultSampler.stdDev, 1.)
    kwargSampler = GaussianSampler(mean=69., stdDev=420.)
    self.assertEqual(kwargSampler.mean, 69.)
    self.assertEqual(kwargSampler.stdDev, 420.)

  def test_values(self, ) -> None:
    """
    This method inspects generated values from 'GaussianSampler' instances
    and verifies that values are generated reasonably as demanded by the
    specified 'mean' and 'stdDev' attributes. Specifically, that no value
    generated is further than 8 standard deviations from the mean. The
    class uses the 'random' module to generate random values and assumes
    functionality as advertised.
    """
    sampler = GaussianSampler(69., 420.)
    numbers = self.rollSampler(sampler)
    minNumber, maxNumber = min(numbers), max(numbers)
    self.assertGreaterEqual(minNumber, sampler.mean - 8 * sampler.stdDev)
    self.assertLessEqual(maxNumber, sampler.mean + 8 * sampler.stdDev)

  def test_str_repr(self, ) -> None:
    """
    This method tests the string representation of 'GaussianSampler'
    instances
    and verifies that it contains the class name and the specified 'mean' and
    'stdDev' attributes.
    """
    sampler = GaussianSampler(69., 420.)
    strStr = str(sampler)
    reprStr = repr(sampler)
    self.assertIn('GaussianSampler', strStr)
    self.assertIn('mean: 69.0', strStr)
    self.assertIn('stdDev: 420.0', strStr)
    self.assertIn('GaussianSampler', reprStr)
    self.assertIn('69.0', reprStr)
    self.assertIn('420.0', reprStr)

  def test_cast_set(self, ) -> None:
    """
    This method tests the casting of 'mean' and 'stdDev' attributes to
    floats when set with non-float values that can be cast to floats.
    """
    sampler = GaussianSampler()
    sampler.mean = 69 + 0j  # type: ignore[assignment]
    sampler.stdDev = 420 + 0j  # type: ignore[assignment]
    self.assertEqual(sampler.mean, 69.)
    self.assertEqual(sampler.stdDev, 420.)

  def test_bad_value_set(self, ) -> None:
    """
    This method tests the setting of 'mean' and 'stdDev' attributes
    against unacceptable float values such as 'nan' and 'inf'.
    Additionally, 'stdDev' must be non-negative.
    """
    trollFloats = float('nan'), float('inf'), float('-inf')
    sampler = GaussianSampler()
    for trollFloat in trollFloats:
      with self.assertRaises(ValueError):
        sampler.mean = trollFloat
      with self.assertRaises(ValueError):
        sampler.stdDev = trollFloat
    with self.assertRaises(ValueError):
      sampler.stdDev = -1.

  def test_bad_type_set(self, ) -> None:
    """
    This method tests that setting 'mean' and 'stdDev' attributes to
    values that cannot be cast to floats raises a 'TypeException'.
    """

    sampler = GaussianSampler()
    trollTypes = lambda never: 'gonna', 'give', {'you', 'up'}
    for trollType in trollTypes:
      with self.assertRaises(TypeException) as context:
        sampler.mean = trollType  # type: ignore[assignment]
      e = context.exception
      self.assertEqual(e.varName, 'mean')
      self.assertEqual(e.actualObject, trollType)
      self.assertIn(float, e.expectedTypes)
      self.assertIsInstance(e.__cause__, TypeCastException)
      with self.assertRaises(TypeException) as context:
        sampler.stdDev = trollType  # type: ignore[assignment]
      e = context.exception
      self.assertEqual(e.varName, 'stdDev')
      self.assertEqual(e.actualObject, trollType)
      self.assertIn(float, e.expectedTypes)
      self.assertIsInstance(e.__cause__, TypeCastException)

  def test_bad_type_get(self, ) -> None:
    """
    This method tests the type guarding on the getter methods for 'mean'
    and 'stdDev' attributes, which should raise 'TypeException'.
    """

    badGaussian = GaussianSampler()
    object.__setattr__(badGaussian, '__mean_value__', 'sixty-nine')
    with self.assertRaises(TypeException) as context:
      _ = badGaussian.mean
    e = context.exception
    self.assertEqual(e.varName, '__mean_value__')
    self.assertEqual(e.actualObject, 'sixty-nine')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)
    object.__setattr__(badGaussian, '__std_dev__', 'four-twenty')
    with self.assertRaises(TypeException) as context:
      _ = badGaussian.stdDev
    e = context.exception
    self.assertEqual(e.varName, '__std_dev__')
    self.assertEqual(e.actualObject, 'four-twenty')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)

  def test_coverage(self, ) -> None:
    """
    As of writing, two separate methods are under consideration for
    handling fallback values for 'Field' attributes. The legacy handling
    relies on functionality provided directly by the getter methods while
    the newer handling relies on the generalized fallback constructor
    provided by 'BaseSampler'.

    Which handling is still under consideration, but with both present in
    the codebase, the legacy handling will not be covered by the normal
    tests. This method creates a subclass of 'GaussianSampler' that
    disables the generalized fallback constructor handling, allowing
    coverage of the legacy handling.
    """

    class LegacyGaussian(GaussianSampler):
      """
      By reimplementing the keyword argument constructor overload,
      the generalized fallback pattern is disabled, allowing coverage of
      the legacy pattern.
      """

      @overload()
      def __init__(self, **kwargs) -> None:
        pass

    legacySampler = LegacyGaussian()
    expectedMean = LegacyGaussian.__fallback_mean__
    self.assertEqual(legacySampler.mean, expectedMean)
    expectedStdDev = LegacyGaussian.__fallback_std_dev__
    self.assertEqual(legacySampler.stdDev, expectedStdDev)
