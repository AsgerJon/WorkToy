"""
The 'worktoy.work_test.samples' module provides random sample data for
testing purposes in the 'worktoy.work_test' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._base_sample import BaseSample
from ._int_sample import IntSample
from ._float_sample import FloatSample
from ._symbolic_sample import SymbolicSample
from ._word_sample import WordSample
from ._lorem_sample import LoremSample

__all__ = [
  'BaseSample',
  'IntSample',
  'FloatSample',
  'SymbolicSample',
  'WordSample',
  'LoremSample',
  ]
