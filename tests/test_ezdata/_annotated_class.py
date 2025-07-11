"""
AnnotatedClass provides subclasses of EZData that provide slots as
annotations in order to test if EZData correctly interprets them as slots.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData


class AnnotatedClass(EZData):
  """
  AnnotatedClass provides subclasses of EZData that provide slots as
  annotations in order to test if EZData correctly interprets them as slots.
  """

  varA: int
  varB: int
  varC: int


class MidNote1(AnnotatedClass):
  """MidNote1 is a subclass of AnnotatedClass with additional slots."""

  varD: int
  varE: int
  varF: int


class MidNote2(MidNote1):
  """MidNote2 continues from MidNote1 with more slots."""

  varG: int
  varH: int
  varI: int


class MidNote3(MidNote2):
  """MidNote3 continues from MidNote2 with even more slots."""

  varJ: int
  varK: int
  varL: int


class SubNotated(MidNote3):
  """
  SubNotated subclasses AnnotatedClass to test if EZData correctly interprets
  slot as annotations when inherited.
  """

  varM: int
  varN: int
  varO: int
