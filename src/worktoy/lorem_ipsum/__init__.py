"""
The 'worktoy.lorem_ipsum' package provides a simple way to generate
lorem ipsum text for testing and placeholder content. The generators draw
their word and length choices from bounded distributions, so a requested
character count is met exactly.

- COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
- StochasticVariable
- GaussianLengths
- StochasticWord
- BaseGenerator
- Clause
- Sentence
- Paragraph
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._words import COMMON_WORDS, UNCOMMON_WORDS, RARE_WORDS
from ._stochastic_variable import StochasticVariable
from ._gaussian_lengths import GaussianLengths
from ._stochastic_word import StochasticWord
from ._base_generator import BaseGenerator
from ._clause import Clause
from ._sentence import Sentence
from ._paragraph import Paragraph

__all__ = [
  'COMMON_WORDS',
  'UNCOMMON_WORDS',
  'RARE_WORDS',
  'StochasticVariable',
  'GaussianLengths',
  'StochasticWord',
  'BaseGenerator',
  'Clause',
  'Sentence',
  'Paragraph',
]
