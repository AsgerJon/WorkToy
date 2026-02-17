"""
SubClass is a more complicated subclass of RegularClass challenging the
functionality of EZData.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import RegularClass

if TYPE_CHECKING:  # pragma: no cover
  pass


class Mid1(RegularClass):
  """Continues from 'g'"""
  d = 30
  e = 40
  f = 50


class Mid2(Mid1):
  """Continues from 'j'"""
  g = 60
  h = 70
  i = 80


class Mid3(Mid2):
  """Continues from 'm'"""
  j = 90
  k = 100
  l = 110


class SubClass(Mid3):
  """
  SubClass is a more complicated subclass of RegularClass challenging the
  functionality of EZData.
  """
  m = 120
  n = 130
  o = 140
