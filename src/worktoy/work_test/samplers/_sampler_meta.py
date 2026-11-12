"""
SamplerMeta is the metaclass of the samplers, 'BaseMeta' combined with
'ABCMeta'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from abc import ABCMeta

from ...mcls import BaseMeta


class SamplerMeta(BaseMeta, ABCMeta):
  """
  A sampler must supply a value type and a single-sample recipe, and a
  sampler class that leaves either out must give no sampler at all: the
  mistake must show where the sampler is created, not at its first row.
  'abc.ABC' cannot stand beside 'BaseObject', since 'ABCMeta' is outside
  the 'MetaType' family and Python refuses the metaclass conflict, so
  the samplers need one metaclass that is both.

  Implementation
  --------------

  'SamplerMeta' is 'BaseMeta' combined with 'ABCMeta' and nothing else,
  the way the 'mcls' package documents for a metaclass of another
  library. 'BaseMeta' answers first along the resolution order, so a
  sampler body keeps its overloads and class hooks, and 'ABCMeta'
  collects the methods marked with 'abstractmethod'. A class that
  leaves one of them abstract is created all the same, and calling it
  raises 'TypeError' naming the method. 'BaseSampler' is built by it.
  """
