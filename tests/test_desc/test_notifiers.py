"""TestNotifiers tests that descriptors correctly notifies. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import random
from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.meta import BaseObject, overload


class Point(BaseObject):
  """Float valued plane coordinates"""

  x = AttriBox[float]()
  y = AttriBox[float]()
  xPreSet = AttriBox[list]([])
  yPreSet = AttriBox[list]([])
  xOnSet = AttriBox[list]([])
  yOnSet = AttriBox[list]([])
  xGet = AttriBox[list]([])
  yGet = AttriBox[list]([])

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  @overload(complex)
  def __init__(self, xy: complex) -> None:
    self.__init__(xy.real, xy.imag)

  @overload()
  def __init__(self, ) -> None:
    self.__init__(69, 420)

  @x.PRESET
  def _handlePreset(self, oldVal: float, newVal: float) -> None:
    """Handle the preset of x."""
    self.xPreSet.append((self.x, oldVal, newVal))

  @x.ONSET
  def _handleOnset(self, oldVal: float, newVal: float) -> None:
    """Handle the onset of x."""
    self.xOnSet.append((self.x, oldVal, newVal))

  @x.PREGET
  def _handleOnGet(self, val: float) -> None:
    """Handle the onget of x, please note that we do not as for the
    current value as this would cause an infinite loop."""
    self.xGet.append(val)

  @y.PRESET
  def _handlePreset(self, oldVal: float, newVal: float) -> None:
    """Handle the preset of y."""
    self.yPreSet.append((self.y, oldVal, newVal))

  @y.ONSET
  def _handleOnset(self, oldVal: float, newVal: float) -> None:
    """Handle the onset of y."""
    self.yOnSet.append((self.y, oldVal, newVal))

  @y.PREGET
  def _handleOnGet(self, val: float) -> None:
    """Handle the onget of y, please note that we do not as for the
    current value as this would cause an infinite loop."""
    self.yGet.append(val)


class TestNotifiers(TestCase):
  """TestNotifiers tests that descriptors correctly notifies. """

  def setUp(self) -> None:
    """Set up the test."""
    self.point = Point()
    self.shufflePoint = Point(69, 420)

  def test_shuffle(self) -> None:
    """Testing that pre-set events has the first two values identical,
    and on-set events has the first and last values identical."""
    randValues = [random() + random() * 1j for _ in range(69)]
    while randValues:
      value = randValues.pop()
      self.shufflePoint.x = value.real
      self.shufflePoint.y = value.imag
    for event in self.shufflePoint.xPreSet:
      self.assertEqual(event[0], event[1])
    for event in self.shufflePoint.xOnSet:
      self.assertEqual(event[0], event[2])
    for event in self.shufflePoint.yPreSet:
      self.assertEqual(event[0], event[1])
    for event in self.shufflePoint.yOnSet:
      self.assertEqual(event[0], event[2])

  def test_onget_error(self) -> None:
    """Tests that creating a class trying to callback onget will raise an
    error."""
    with self.assertRaises(TypeError):
      class FailClass(BaseObject):
        """LOL"""

        x = AttriBox[float]()

        @x.ONGET
        def _(self) -> None:
          pass
