"""The comparison cohort: one 2D point, implemented several ways.

These classes are deliberately NOT all worktoy-idiomatic. The whole
point is to put worktoy descriptors side by side with the plain,
slotted, and dataclass baselines a skeptic would reach for, so the
ergonomics-versus-speed trade is measured rather than asserted.

Every implementation exposes the same surface: construct from two
floats, read '.x', write '.x'. That keeps the per-operation timings
in '_harness' apples-to-apples across the cohort.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from dataclasses import dataclass

from worktoy.desc import AttriBox, Field
from worktoy.desc._fast_box import FastBox  # noqa  not yet public
from worktoy.dispatch import overload
from worktoy.ezdata import EZData, EZField
from worktoy.mcls import BaseObject


class PlainPoint:
  """Baseline: an ordinary class with an instance '__dict__'."""

  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y


class SlotsPoint:
  """Baseline: the fast hand-written class, slotted, no '__dict__'."""

  __slots__ = ('x', 'y')

  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y


@dataclass
class DataPoint:
  """Baseline: a stdlib dataclass (synthesised '__init__')."""

  x: float
  y: float


class EZPoint(EZData):
  """worktoy: EZData. Slotted storage, generated '__init__'."""

  x = EZField[float](0.0)
  y = EZField[float](0.0)


class BoxPoint(BaseObject):
  """worktoy: BaseObject with 'AttriBox' descriptors and an
  overloaded constructor. The realistic worktoy spelling."""

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y


class FastPoint:
  """worktoy: a plain hand-written class with 'FastBox' descriptors.
  No metaclass, no context, no hooks. The lean opt-in option."""

  x = FastBox[float](0.0)
  y = FastBox[float](0.0)

  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y


class FieldPoint(BaseObject):
  """worktoy: BaseObject with 'Field' descriptors backed by private
  values and explicit get/set accessors."""

  __x_value__: float = 0.0
  __y_value__: float = 0.0

  x: Field[float] = Field()
  y: Field[float] = Field()

  @x.GET
  def _getX(self) -> float:
    return self.__x_value__

  @x.SET
  def _setX(self, value: float) -> None:
    self.__x_value__ = value

  @y.GET
  def _getY(self) -> float:
    return self.__y_value__

  @y.SET
  def _setY(self, value: float) -> None:
    self.__y_value__ = value

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y
