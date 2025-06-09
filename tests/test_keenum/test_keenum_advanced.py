"""
Tests more advanced features of KeeNum.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import auto, KeeNum

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class Fruit(KeeNum):
  APPLE = auto()
  BANANA = auto('Yellow')
  CHERRY = auto('Red')


class Vehicle(KeeNum):
  CAR = auto()
  BIKE = "manual"  # Not a member
  BUS = auto()


class ValidStrings(KeeNum):
  A = auto('x')
  B = auto('y')


class Wrapper:
  def __init__(self, val: int) -> None:
    self.val = val

  def __str__(self) -> str:
    return '<Wrapper with value: %d>' % self.val

  def __repr__(self) -> str:
    return 'Wrapper(%d)' % self.val


w1 = Wrapper(1)
w2 = Wrapper(2)


class Wrapped(KeeNum):
  FIRST = auto(w1)
  SECOND = auto(w2)


class Steps(KeeNum):
  STEP1 = auto()
  STEP2 = auto()
  STEP3 = auto()


import unittest


class TestKeeNum(unittest.TestCase):

  def test_ad_hoc(self) -> None:
    """
    Ad hoc testing
    """
    classes = [Fruit, Vehicle, ValidStrings, Wrapped, Steps]
    for cls in classes:
      print('_' * 77)
      print('--- Testing class: %s ---' % cls.__name__)
      for item in cls:
        infoSpec = """%d: name: %s, value: %s"""
        info = infoSpec % (item.index, item.name, item.value)
        if len(info) > 77:
          print('%s...' % info[:74])
          continue
        print(info)
      print('¨' * 77)

  def test_namesValuesIndexes(self) -> None:
    self.assertEqual(Fruit.APPLE.name, 'APPLE')
    self.assertEqual(Fruit.APPLE.value, 'APPLE')
    self.assertEqual(Fruit.APPLE.index, 0)
    self.assertEqual(Fruit.BANANA.value, 'Yellow')
    self.assertEqual(Fruit.BANANA.index, 1)
    self.assertEqual(Fruit.CHERRY.index, 2)

  def test_nonAutoEntriesIgnored(self) -> None:
    self.assertTrue(hasattr(Vehicle, 'BIKE'))
    self.assertNotIn('BIKE', Vehicle.__member_entries__)
    self.assertEqual([v.name for v in Vehicle], ['CAR', 'BUS'])

  def test_valueTypeConsistency(self) -> None:
    try:
      class Mixed(KeeNum):
        A = auto('valid')
        B = auto(123)
    except Exception as exception:
      print("""Exception raised: %s""" % str(exception))
    else:
      print("""No exception raised, but expected one!""")

  def test_iterationOrder(self) -> None:
    names = [step.name for step in Steps]
    self.assertEqual(names, ['STEP1', 'STEP2', 'STEP3'])

  def test_customObjectValues(self) -> None:
    self.assertEqual(Wrapped.FIRST.value.val, 1)
    self.assertEqual(Wrapped.SECOND.value.val, 2)
