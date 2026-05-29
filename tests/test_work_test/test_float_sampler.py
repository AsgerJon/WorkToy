"""
TestFloatSampler tests the FloatSampler class from the
'worktoy.work_test.samplers' module.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException
from worktoy.work_test.samplers import FloatSampler
from . import SamplerTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestFloatSampler(SamplerTest):
  """
  TestFloatSampler tests the FloatSampler class from the
  'worktoy.work_test.samplers' module.
  """

  def test_init(self, ) -> None:
    """
    This method tests the constructor overloads of the 'FloatSampler'
    class, which are as follows:

    @overload(float, float, )
    def __init__(self, minVal: float, maxVal: float, **kw) -> None: ...

    @overload(float, )
    def __init__(self, maxVal: float, **kw) -> None: ...

    @overload()
    def __init__(self, **kw) -> None: ...
    """

    floatFloatKwarg = FloatSampler(69., 420., lmao=True)
    self.assertEqual(floatFloatKwarg.minVal, 69.)
    self.assertEqual(floatFloatKwarg.maxVal, 420.)
    floatFloatSampler = FloatSampler(69., 420.)
    self.assertEqual(floatFloatSampler.minVal, 69.)
    self.assertEqual(floatFloatSampler.maxVal, 420.)
    floatKwarg = FloatSampler(69., breh=False)
    self.assertEqual(floatKwarg.minVal, 0.)
    self.assertEqual(floatKwarg.maxVal, 69.)
    floatSampler = FloatSampler(69.)
    self.assertEqual(floatSampler.minVal, 0.)
    self.assertEqual(floatSampler.maxVal, 69.)
    defaultSampler = FloatSampler()
    self.assertEqual(defaultSampler.minVal, 0.)
    self.assertEqual(defaultSampler.maxVal, 1.)
    kwargSampler = FloatSampler(minVal=69., maxVal=420.)
    self.assertEqual(kwargSampler.minVal, 69.)
    self.assertEqual(kwargSampler.maxVal, 420.)

  def test_values(self, ) -> None:
    """
    The 'FloatSampler' class inherits most functionality from 'IntSampler'
    tested elsewhere, so this method tests only the values it generates.
    Specifically, it validates that it adheres to the specified value
    given by the 'minValue' and 'maxValue' attributes.
    """
    sampler = FloatSampler(69., 420.)
    numbers = self.rollSampler(sampler)
    minNumber, maxNumber = min(numbers), max(numbers)
    self.assertGreaterEqual(minNumber, sampler.minVal)
    self.assertLessEqual(maxNumber, sampler.maxVal)

  def test_bad_set(self, ) -> None:
    """
    This method tests the handling of bad types when setting 'minVal' and
    'maxVal' attributes. The 'FloatSampler' class should raise
    'TypeException'
    when trying to set these attributes to non-float values.
    """
    sampler = FloatSampler()
    with self.assertRaises(TypeException) as context:
      sampler.minVal = 'sixty-nine'  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.varName, 'minValue')
    self.assertEqual(e.actualObject, 'sixty-nine')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)

    with self.assertRaises(TypeException) as context:
      sampler.maxVal = 'four-twenty'  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.varName, 'maxValue')
    self.assertEqual(e.actualObject, 'four-twenty')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)

  def test_bad_get(self, ) -> None:
    """
    This method tests the handling of bad types when getting 'minVal' and
    'maxVal' attributes. The 'FloatSampler' class should raise
    'TypeException'
    when trying to get these attributes if they are set to non-float values.
    """
    sampler = FloatSampler()
    object.__setattr__(sampler, '__min_value__', 'sixty-nine')
    with self.assertRaises(TypeException) as context:
      _ = sampler.minVal
    e = context.exception
    self.assertEqual(e.varName, 'minVal')
    self.assertEqual(e.actualObject, 'sixty-nine')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)

    object.__setattr__(sampler, '__max_value__', 'four-twenty')
    with self.assertRaises(TypeException) as context:
      _ = sampler.maxVal
    e = context.exception
    self.assertEqual(e.varName, 'maxVal')
    self.assertEqual(e.actualObject, 'four-twenty')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)
