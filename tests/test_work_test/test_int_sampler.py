"""
TestIntSample subclasses 'SampleTest' and provides test cases for the
'IntSample' class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.work_test.samplers import IntSampler
from . import SamplerTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestIntSampler(SamplerTest):
  """
  TestIntSample provides test cases for the 'IntSample' class.
  """

  def test_init(self, ) -> None:
    """
    This method test the different instantiations of the 'IntSample' class
    having the following overload signatures:


    @overload(int, int, strict=True)
    def __init__(self, minVal: int, maxVal: int, **kw) -> None: ...

    @overload(int, strict=True)
    def __init__(self, val: int, **kw) -> None: ...

    @overload()
    def __init__(self, **kw) -> None: ...
    """
    argsTuple = (
      (69, 420),
      (69, 420,),
      (1337,),
      (69,),
      (),
      (),
    )
    kwargsTuple = (
      dict(),
      dict(lmao=True),
      dict(),
      dict(maxVal=420),
      dict(minVal=42, maxVal=69),
      dict(),
    )
    for args, kwargs in zip(argsTuple, kwargsTuple):
      sampler = IntSampler(*args, **kwargs)
      samples = self.rollSampler(sampler)
      minSample, maxSample = min(samples), max(samples)
      self.assertLessEqual(sampler.minVal, minSample)
      self.assertGreaterEqual(sampler.maxVal, maxSample)

  def test_bad_init(self, ) -> None:
    """
    This method tests the handling of bad type arguments. For positional
    arguments having bad types, the overloading mechanism should fail with
    'DispatchException', but for keyword arguments, the overloading
    mechanism has already resolved. Thus, instead of the
    'DispatchException', the dispatching overload itself raises
    'TypeException'.
    """
    #  Arguments matching no overload signature
    args = 'never', 'gonna', 'give', 'you', 'up'
    with self.assertRaises(DispatchException) as context:
      _ = IntSampler(*args)  # noqa
    e = context.exception
    self.assertIs(e.dispatch, IntSampler.__dict__['__init__'])
    for expected, actual in zip(args, e.args):
      self.assertEqual(expected, actual)

    #  Keyword arguments assigning bad types
    with self.assertRaises(TypeException) as context:
      _ = IntSampler(minVal='sixty-nine', maxVal='four-twenty')  # noqa
    e = context.exception
    self.assertIn(e.varName, ('minVal', 'maxVal'))
    self.assertIn(e.actualObject, ('sixty-nine', 'four-twenty'))
    self.assertIs(e.actualType, str)
    self.assertIn(int, e.expectedTypes)

  def test_set_range(self, ) -> None:
    """
    This method tests changes to the 'minVal' and 'maxVal' attributes
    collectively described as 'range'.
    """
    sampler = IntSampler()
    sampler.minVal = 69
    sampler.maxVal = 420
    samples = self.rollSampler(sampler, )
    minSample, maxSample = min(samples), max(samples)
    self.assertLessEqual(sampler.minVal, minSample)
    self.assertGreaterEqual(sampler.maxVal, maxSample)

  def test_reversed_range(self, ) -> None:
    """
    This method tests the handling of setting 'minVal' to a new value
    greater than 'maxVal'. The intention is for the sampler to set the new
    'minVal' to the existing 'maxVal' and the new 'maxVal' to the new value.
    """

    sampler = IntSampler(-1337, -69)
    sampler.minVal = 69  # Should set range to (-69, 69)
    samples = self.rollSampler(sampler)
    minSample, maxSample = min(samples), max(samples)
    self.assertLessEqual(sampler.minVal, minSample)
    self.assertGreaterEqual(sampler.maxVal, maxSample)
    sampler.minVal = 420  # Should set range to (69, 420)
    samples = self.rollSampler(sampler)
    minSample, maxSample = min(samples), max(samples)
    self.assertLessEqual(sampler.minVal, minSample)
    self.assertGreaterEqual(sampler.maxVal, maxSample)

    sampler = IntSampler(1000, 1337)
    sampler.maxVal = 420  # Should set range to (420, 1000)
    samples = self.rollSampler(sampler)
    minSample, maxSample = min(samples), max(samples)
    self.assertLessEqual(sampler.minVal, minSample)
    self.assertGreaterEqual(sampler.maxVal, maxSample)
    sampler.maxVal = 69  # Should set range to (69, 420)
    samples = self.rollSampler(sampler)
    minSample, maxSample = min(samples), max(samples)
    self.assertLessEqual(sampler.minVal, minSample)
    self.assertGreaterEqual(sampler.maxVal, maxSample)

  def test_bad_range(self, ) -> None:
    """
    Testing the exceptions raised, when bad types or values are set on
    the 'sampler.minVal' and 'sampler.maxVal' attributes.
    """
    sampler = IntSampler()
    with self.assertRaises(TypeException) as context:
      sampler.minVal = 'sixty-nine'  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.varName, 'minVal')
    self.assertEqual(e.actualObject, 'sixty-nine')
    self.assertIs(e.actualType, str)
    self.assertIn(int, e.expectedTypes)

    with self.assertRaises(TypeException) as context:
      sampler.maxVal = 'four-twenty'  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.varName, 'maxVal')
    self.assertEqual(e.actualObject, 'four-twenty')
    self.assertIs(e.actualType, str)
    self.assertIn(int, e.expectedTypes)

  def test_cast_range(self, ) -> None:
    """
    This method tests that 'minVal' and 'maxVal' can be cast to 'int'.
    """
    sampler = IntSampler()
    sampler.minVal = 69.0
    sampler.maxVal = 420.0
    self.assertEqual(sampler.minVal, 69)
    self.assertEqual(sampler.maxVal, 420)

    sampler = IntSampler()
    sampler.minVal = '69'
    sampler.maxVal = '420'
    self.assertEqual(sampler.minVal, 69)
    self.assertEqual(sampler.maxVal, 420)
