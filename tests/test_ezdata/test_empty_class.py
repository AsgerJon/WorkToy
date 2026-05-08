"""Integration tests for ``EZData`` subclasses with no fields."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData
from worktoy.waitaminute.ez import UnfrozenHashException
from . import EZTest


class TestEmptyClass(EZTest):

  def test_empty_class_construct(self) -> None:
    class Empty(EZData):
      pass

    obj = Empty()
    self.assertEqual(len(obj), 0)
    self.assertEqual(list(obj), [])
    self.assertEqual(repr(obj), 'Empty()')

  def test_empty_class_eq(self) -> None:
    class Empty(EZData):
      pass

    self.assertEqual(Empty(), Empty())

  def test_empty_frozen_hashable(self) -> None:
    class EmptyFrozen(EZData, frozen=True):
      pass

    self.assertEqual(hash(EmptyFrozen()), hash(EmptyFrozen()))

  def test_empty_unfrozen_hash_raises(self) -> None:
    class EmptyMutable(EZData):
      pass

    with self.assertRaises(UnfrozenHashException) as ctx:
      hash(EmptyMutable())
    self.assertEqual(ctx.exception.className, 'EmptyMutable')
