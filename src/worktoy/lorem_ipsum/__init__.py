"""
The 'worktoy.lorem_ipsum' package provides a simple way to generate
lorem ipsum text for testing and placeholder content.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._words import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from ._base_generator import BaseGenerator
from ._stochastic_word import StochasticWord
from ._clause import Clause
from ._sentence import Sentence
from ._paragraph import Paragraph

__all__ = [
  'COMMON_WORDS',
  'UNCOMMON_WORDS',
  'RARE_WORDS',
  'BaseGenerator',
  'StochasticWord',
  'Clause',
  'Sentence',
  'Paragraph',
]
