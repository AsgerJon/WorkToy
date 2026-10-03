"""
TestStochasticWordGap subclasses 'LoremIpsumTest' and pins that a
'StochasticWord' subclass whose words leave a length out between the
shortest and the longest is refused at its class statement. The draw of
a length assumes every length in that range has words, and nothing
checked it, so such a subclass raised 'IndexError' from 'realize' at
random.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticWord

from . import LoremIpsumTest


class TestStochasticWordGap(LoremIpsumTest):
  """
  TestStochasticWordGap provides tests for the word lengths of a
  'StochasticWord' subclass.
  """

  def test_gap_refused(self) -> None:
    """Words of lengths 2, 6 and 8 are refused, naming a missing
    length."""
    with self.assertRaises(ValueError) as context:
      class Gappy(StochasticWord):
        __category_weights__ = ((('ab', 'abcdef', 'abcdefgh'), 1.0),)
    self.assertIn('Gappy', str(context.exception))
    self.assertIn('3', str(context.exception))

  def test_gapless_accepted(self) -> None:
    """Words covering every length from the shortest to the longest are
    accepted and realize words of those lengths."""

    class Gapless(StochasticWord):
      __category_weights__ = ((('ab', 'abc', 'abcd'), 1.0),)

    word = Gapless()
    for _ in range(50):
      self.assertIn(len(word.realize()), (2, 3, 4))
