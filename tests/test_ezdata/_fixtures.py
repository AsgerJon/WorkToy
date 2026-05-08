"""Shared ``EZData`` fixtures used by the integration tests."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData


class Point(EZData):
  x = 0
  y = 0


class Annotated(EZData):
  name: str = 'anon'
  age: int = 0


class Frozen(EZData, frozen=True):
  r = 0
  g = 0
  b = 0


class Ordered(EZData, order=True):
  a = 0
  b = 0
  c = 0


class FrozenOrdered(EZData, frozen=True, order=True):
  a = 0
  b = 0


class Mixed3(EZData):
  x = 0
  y = 1
  note = 'hi'


class Sub3D(Point):
  z = 0
