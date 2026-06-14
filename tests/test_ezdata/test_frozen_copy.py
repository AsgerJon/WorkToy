"""
TestFrozenCopy subclasses 'EZTest' from the 'tests.test_ezdata' package
and pins that frozen 'EZData' instances survive 'copy' and 'deepcopy'. A
frozen class rejects every assignment through its generated '__setattr__',
so the default reconstruction (build a blank instance, then set each
slot) raises. The generated '__copy__' and '__deepcopy__' write the
field values through 'object.__setattr__' instead, so a frozen instance
clones faithfully, matching the behaviour of a frozen dataclass.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import copy, deepcopy

from worktoy.ezdata import EZData, EZField

from . import EZTest


class FrozenPt(EZData, frozen=True):
  """FrozenPt is a frozen point used by the copy probes."""

  x = EZField[int](0)
  y = EZField[int](0)


class FrozenBag(EZData, frozen=True):
  """FrozenBag holds a mutable field, exercising the deep copy path."""

  items = EZField[list]()


class TestFrozenCopy(EZTest):
  """
  TestFrozenCopy provides tests for 'copy' and 'deepcopy' of frozen
  'EZData' instances.
  """

  def test_copy_returns_equal_clone(self) -> None:
    """A shallow copy of a frozen instance is a distinct but equal
    instance of the same class."""
    original = FrozenPt(3, 4)
    clone = copy(original)
    self.assertIsNot(clone, original)
    self.assertEqual(clone, original)
    self.assertIsInstance(clone, FrozenPt)

  def test_deepcopy_returns_equal_clone(self) -> None:
    """A deep copy of a frozen instance is a distinct but equal
    instance, with field values preserved."""
    original = FrozenPt(3, 4)
    clone = deepcopy(original)
    self.assertIsNot(clone, original)
    self.assertEqual(clone, original)
    self.assertEqual(clone.x, 3.0)
    self.assertEqual(clone.y, 4.0)

  def test_deepcopy_inside_container(self) -> None:
    """A frozen instance carried inside a deep-copied container survives
    as an equal instance."""
    config = {'pt': FrozenPt(3, 4)}
    self.assertEqual(deepcopy(config)['pt'], FrozenPt(3, 4))

  def test_clone_stays_frozen(self) -> None:
    """A clone of a frozen instance is itself frozen and rejects
    assignment."""
    clone = deepcopy(FrozenPt(1, 2))
    with self.assertRaises(AttributeError):
      clone.x = 99

  def test_deepcopy_mutable_field_is_independent(self) -> None:
    """A deep copy of a frozen instance gives the clone its own copy of a
    mutable field, so mutating the clone's list does not touch the
    original's."""
    original = FrozenBag([1, 2, 3])
    clone = deepcopy(original)
    self.assertIsNot(clone.items, original.items)
    clone.items.append(99)
    self.assertEqual(original.items, [1, 2, 3])

  def test_shallow_copy_shares_mutable_field(self) -> None:
    """A shallow copy shares the mutable field object, matching the
    contract of 'copy.copy'."""
    original = FrozenBag([1, 2, 3])
    clone = copy(original)
    self.assertIs(clone.items, original.items)
