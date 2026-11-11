"""
PromiseValidSlice promises 'ValidSlice' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import ValidSlice


class PromiseValidSlice(TestCase):
  """
  'isinstance(s, ValidSlice)' is True exactly when 's' is a slice whose
  start, stop and step are each 'None', an 'int', or an object whose
  type has a callable '__index__'. The '__index__' is not called, so
  one that would raise still passes. 'ValidSlice' itself cannot be
  instantiated and raises 'TypeError'. Source: the 'ValidSlice'
  docstring and its examples.
  """

  def test_valid(self) -> None:
    class Position:
      def __index__(self) -> int:
        return 1

    class Broken:
      def __index__(self) -> int:
        raise RuntimeError('never called by ValidSlice')

    self.assertIsInstance(slice(1), ValidSlice)
    self.assertIsInstance(slice(None, None, None), ValidSlice)
    self.assertIsInstance(slice(0, Position(), 2), ValidSlice)
    self.assertIsInstance(slice(Broken()), ValidSlice)

  def test_invalid(self) -> None:
    self.assertNotIsInstance(slice('not a slice'), ValidSlice)
    self.assertNotIsInstance(slice(0, 10, 'step'), ValidSlice)
    self.assertNotIsInstance((0, 10), ValidSlice)

  def test_not_instantiable(self) -> None:
    with self.assertRaises(TypeError):
      ValidSlice()
