"""
The 'worktoy.utilities.lorem_ipsum' package provides a simple way to generate
lorem ipsum text for testing and placeholder content.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._base_generator import BaseGenerator
from ._stochastic_word import StochasticWord
from ._clause import Clause
from ._sentence import Sentence
from ._paragraph import Paragraph

__all__ = [
  'BaseGenerator',
  'StochasticWord',
  'Clause',
  'Sentence',
  'Paragraph',
  ]
