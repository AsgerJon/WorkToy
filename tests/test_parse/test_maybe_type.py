"""TestMaybeType tests the 'maybeType' function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from string import ascii_lowercase, digits, ascii_uppercase
from random import randint, random, choices
from types import FunctionType
from typing import Any, Callable
from unittest import TestCase

from worktoy.parse import maybe, maybeType


class TestMaybeType(TestCase):
  """TestMaybeType tests the 'maybeType' function."""

  @staticmethod
  def getIntSample() -> int:
    """Return an integer sample."""
    return randint(0, 255)

  @staticmethod
  def getFloatSample(scale: float = None) -> float:
    """Return a float sample."""
    scale = maybe(scale, 1.0)
    return random() * scale

  @staticmethod
  def getStringSample(n: int = None) -> str:
    """Return a string sample."""
    chars = '%s%s%s' % (ascii_lowercase, digits, ascii_uppercase)
    n = maybe(n, 16)
    chars = [c for c in chars]
    out = []
    for _ in range(n):
      out.append(choices(chars, k=1)[0])
    return ''.join(out)

  @staticmethod
  def getCallableSample() -> Callable:
    """Return a callable sample."""

    def sampleFunc(*args) -> Any:
      """A sample function."""
      return args

    types = [int, float, str, list, dict, tuple]
    existing = getattr(sampleFunc, '__annotations__', )
    existing = {**existing, **{'return': choices(types, k=1)}}
    setattr(sampleFunc, '__annotations__', existing)
    return sampleFunc

  @staticmethod
  def getListSample(n: int = None) -> list:
    """Return a list sample."""
    n = maybe(n, 16)
    out = []
    for _ in range(n):
      s = random()
      if s < 0.25:
        out.append(TestMaybeType.getIntSample())
      elif s < 0.5:
        out.append(TestMaybeType.getFloatSample())
      elif s < 0.75:
        out.append(TestMaybeType.getStringSample())
      else:
        out.append(TestMaybeType.getCallableSample())
    return out

  def getTupleSample(self, n: int = None) -> tuple:
    """Return a tuple sample."""
    n = maybe(n, 16)
    s = random()
    if s < 0.25:
      return tuple([self.getIntSample() for _ in range(n)])
    if s < 0.5:
      return tuple([self.getFloatSample() for _ in range(n)])
    if s < 0.75:
      return tuple([self.getStringSample() for _ in range(n)])
    return tuple([self.getCallableSample() for _ in range(n)])

  def getGenSample(self, ) -> Any:
    """Return a generator sample."""
    out = [self.getListSample(),
           self.getTupleSample(),
           self.getCallableSample(), ]
    for _ in range(16):
      s = random()
      if 2 * s > 1:
        for item in self.getListSample(16):
          out.append(item)
          if random() < 0.5:
            out.append(None)
      else:
        out.append(None)
    return [item for item in out]

  def testInt(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    sample = [None, None, 77, None]
    self.assertEqual(77, maybeType(int, *sample))

  def testFloat(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    sample = [None, None, 77.77, None]
    self.assertEqual(77.77, maybeType(float, *sample))

  def testStr(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    sample = [None, None, '77', None]
    self.assertEqual('77', maybeType(str, *sample))

  def testList(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    sample = [None, None, [77, 69, 420], None]
    self.assertEqual([77, 69, 420], maybeType(list, *sample))

  def testTuple(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    sample = [None, None, (77, 69, 420), None]
    self.assertEqual((77, 69, 420), maybeType(tuple, *sample))

  def testDict(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    sample = [None, None, {77: 69, 420: 666}, None]
    self.assertEqual({77: 69, 420: 666}, maybeType(dict, *sample))
    self.assertIsInstance(maybeType(dict, *sample), dict)

  def testCallable(self, ) -> None:
    """Test the 'maybeType' function with a single type."""
    callMeMaybe = self.getCallableSample()
    sample = [None, None, callMeMaybe, None]
    self.assertEqual(callMeMaybe, maybeType(FunctionType, *sample))

  def testNameInt(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    sample = [None, None, 77, None]
    self.assertEqual(77, maybeType('int', *sample))

  def testNameFloat(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    sample = [None, None, 77.77, None]
    self.assertEqual(77.77, maybeType('float', *sample))

  def testNameStr(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    sample = [None, None, '77', None]
    self.assertEqual('77', maybeType('str', *sample))

  def testNameList(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    sample = [None, None, [77, 69, 420], None]
    self.assertEqual([77, 69, 420], maybeType('list', *sample))

  def testNameTuple(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    sample = [None, None, (77, 69, 420), None]
    self.assertEqual((77, 69, 420), maybeType('tuple', *sample))

  def testNameDict(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    sample = [None, None, {77: 69, 420: 666}, None]
    self.assertEqual({77: 69, 420: 666}, maybeType('dict', *sample))
    self.assertIsInstance(maybeType('dict', *sample), dict)

  def testNameCallable(self, ) -> None:
    """Test the 'maybeType' function with a single name."""
    callMeMaybe = self.getCallableSample()
    sample = [None, None, callMeMaybe, None]
    self.assertEqual(callMeMaybe, maybeType('function', *sample))

  def testTypes(self, ) -> None:
    """Test the 'maybeType' function with a tuple of types."""
    sample = [None, None, 77.77, None]
    self.assertEqual(77.77, maybeType((int, float, str), *sample))
    sample = [None, None, 77, None]
    self.assertEqual(77, maybeType((int, float, str), *sample))
    sample = [None, None, '77', None]
    self.assertEqual('77', maybeType((int, float, str), *sample))
