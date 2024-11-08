"""EZData creates data classes inline. These are derived directly from the
FastMeta metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZMeta, EZBase, EZBox

try:
  from typing import Any
except ImportError:
  Any = object

from worktoy.base import FastMeta, FastSpace, overload
from worktoy.desc import AttriBox
from worktoy.meta import BaseMetaclass


class EZData(FastMeta):
  """EZData creates data classes inline. These are derived directly from the
  FastMeta metaclass. """
