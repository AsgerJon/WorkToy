"""TestCallMeMaybe tests if CallMeMaybe correctly identifies functions and
function-like objects. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from time import sleep
from typing import Any
from unittest import TestCase

from worktoy.desc import CoreDescriptor
from worktoy.meta import BaseObject, overload, CallMeMaybe


class Decorator(CoreDescriptor):
  """Instances of this decorator can be applied to both classes and
  functions using 'overload' to dispatch the correct '__call__' method. """

  def __init__(self, name: str) -> None:
    """Initializes the decorator with a name."""
    self.__test_name__ = name

  @overload(CallMeMaybe)
  def __call__(self, callMeMaybe: CallMeMaybe) -> CallMeMaybe:
    """Expects a function-like object"""
    setattr(callMeMaybe, self.__test_name__, 'function')
    return callMeMaybe

  @overload(type)
  def __call__(self, cls: type) -> type:
    """Expects a class"""
    setattr(cls, self.__test_name__, 'type')
    return cls

  @overload()
  def __call__(self, ) -> None:
    """Expects nothing"""
    print('LOL')


class TestCallMeMaybe(TestCase):
  """TestCallMeMaybe tests if CallMeMaybe correctly identifies functions and
  function-like objects. """

  nameTest = Decorator('testName')

  @nameTest
  def someMethod(self) -> None:
    """Decorated method"""
    pass

  @nameTest
  class SomeClass:
    """Decorated class"""
    pass

  @classmethod
  def setUpClass(cls: TestCase) -> None:
    """Sets up the test class"""
    cls.lambdaType = type(lambda: None)

    def _func() -> None:
      """Sample Function"""

    cls.funcType = type(_func)

  def test_isinstance(self, ) -> None:
    """Testing that isinstance works in basic examples. """
    lambdaSample = lambda: None

    def funcSample() -> None:
      pass

    class CallableSample:
      def __call__(self, ) -> None:
        pass

    class DontCallSample:
      pass

    self.assertIsInstance(lambda: None, CallMeMaybe)
    self.assertIsInstance(funcSample, CallMeMaybe)
    self.assertIsInstance(CallableSample(), CallMeMaybe)
    self.assertNotIsInstance(DontCallSample(), CallMeMaybe)
    self.assertNotIsInstance('Not a function', CallMeMaybe)
    self.assertNotIsInstance(69420, CallMeMaybe)

  def test_issubclass(self) -> None:
    """Testing that issubclass works in basic examples. """
    self.assertTrue(issubclass(self.funcType, CallMeMaybe))
    self.assertTrue(issubclass(self.lambdaType, CallMeMaybe))

  def test_usage(self) -> None:
    """Testing that the decorator works as expected. """
    self.assertEqual(getattr(self.someMethod, 'testName', ), 'function')
    self.assertEqual(getattr(self.SomeClass, 'testName', ), 'type')
