"""The dispatch cohort: one method taking an 'int', a 'float' or a
'WeekDay', written the ways Python offers and as worktoy overloads.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from functools import singledispatch

from worktoy.dispatch import overload
from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseObject


class WeekDay(KeeNum):
  """An enumeration, as a third type to dispatch on."""

  MONDAY = Kee[str]('mandag')
  TUESDAY = Kee[str]('tirsdag')


class Plain:
  """Baseline: a method that looks at nothing."""

  def f(self, x: object) -> object:
    return x


class ByHand:
  """Baseline: the chain of 'isinstance' tests a project writes by
  hand where it has no overloads."""

  def f(self, x: object) -> object:
    if isinstance(x, int):
      return x
    if isinstance(x, float):
      return x
    if isinstance(x, WeekDay):
      return x
    raise TypeError(x)


@singledispatch
def single(x: object) -> object:
  """Baseline: 'functools.singledispatch', Python's own dispatch on the
  type of one argument."""
  raise TypeError(x)


@single.register(int)
def _singleInt(x: int) -> object:
  return x


@single.register(float)
def _singleFloat(x: float) -> object:
  return x


@single.register(WeekDay)
def _singleDay(x: WeekDay) -> object:
  return x


class Loaded(BaseObject):
  """worktoy: overloads. 'f' takes each type exactly; 'g' has no 'int'
  overload, so an 'int' reaches its 'float' overload by widening."""

  @overload(int)
  def f(self, x: int) -> object:
    return x

  @overload(float)
  def f(self, x: float) -> object:
    return x

  @overload(WeekDay)
  def f(self, x: WeekDay) -> object:
    return x

  @overload(str, str)
  def f(self, a: str, b: str) -> object:
    return a

  @overload(float)
  def g(self, x: float) -> object:
    return x

  @overload(str, str)
  def g(self, a: str, b: str) -> object:
    return a
