"""
Tests more advanced features of KeeNum.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import KeeTest

from worktoy.keenum import auto, KeeNum

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class Fruit(KeeNum):
  APPLE = auto()
  BANANA = auto('Yellow')
  CHERRY = auto('Red')


class Vehicle(KeeNum):
  CAR = auto()
  BIKE = auto()
  BUS = auto()


class ValidStrings(KeeNum):
  A = auto('x')
  B = auto('y')


class Wrapper:
  def __init__(self, val: int) -> None:
    self.val = val

  def __str__(self) -> str:
    return '<Wrapper with value: %d>' % self.val

  __repr__ = __str__


w1 = Wrapper(1)
w2 = Wrapper(2)


class Wrapped(KeeNum):
  FIRST = auto(w1)
  SECOND = auto(w2)


class Steps(KeeNum):
  STEP1 = auto()
  STEP2 = auto()
  STEP3 = auto()


class TestKeeNum(KeeTest):

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_namesValuesIndexes(self) -> None:
    self.assertEqual(Fruit.APPLE.name, 'APPLE')
    self.assertEqual(Fruit.APPLE.value.upper(), 'APPLE')
    self.assertEqual(Fruit.APPLE.index, 0)
    self.assertEqual(Fruit.BANANA.value.lower(), 'yellow')
    self.assertEqual(Fruit.BANANA.index, 1)
    self.assertEqual(Fruit.CHERRY.index, 2)

  def test_iterationOrder(self) -> None:
    names = [step.name for step in Steps]
    self.assertEqual(names, ['STEP1', 'STEP2', 'STEP3'])

  def test_customObjectValues(self) -> None:
    self.assertEqual(Wrapped.FIRST.value.val, 1)
    self.assertEqual(Wrapped.SECOND.value.val, 2)

  def test_str_repr(self) -> None:
    """
    Tests the __str__ on the Wrapper instances
    """

    self.assertEqual(str(Wrapped.FIRST.value), repr(Wrapped.FIRST.value))
