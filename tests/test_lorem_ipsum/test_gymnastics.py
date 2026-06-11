"""
TestGymnastics subclasses 'LoremIpsumTest' and provides tests that reach
for those difficult to cover edges.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import StochasticVariable
from . import LoremIpsumTest


class TestGymnastics(LoremIpsumTest):
  """
  TestGymnastics subclasses 'LoremIpsumTest' and provides tests that reach
  for those difficult to cover edges.
  """

  def test_stupid_class_init(self, ) -> None:
    """
    Testing that the underlying '__class_init__' raises 'AttributeError'
    when handed a plain 'dict' in place of the expected namespace object.
    """
    init = StochasticVariable.__class_init__
    init = getattr(init, '__func__', init)
    with self.assertRaises(AttributeError):
      _ = init(object, '_', (), dict())

  def test_not_implemented_method(self) -> None:
    """
    Testing that the 'StochasticVariable' raises 'NotImplementedError' when
    its 'sampleInteger' method is called.
    """
    with self.assertRaises(NotImplementedError):
      _ = StochasticVariable().sampleInteger()
