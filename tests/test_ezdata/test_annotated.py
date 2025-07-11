"""
TestAnnotated tests the functionality of EZData classes with every slot
annotated rather than being class variables.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import AnnotatedClass, MidNote1, MidNote2, MidNote3, SubNotated
from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestAnnotated(EZTest):
  """
  TestAnnotated tests the functionality of EZData classes with every slot
  annotated rather than being class variables.
  """

  def test_slots(self) -> None:
    """Tests that classes has the correct slots."""
    annotatedSlots = 'ABC'
    mid1Slots = 'ABCDEF'
    mid2Slots = 'ABCDEFGHI'
    mid3Slots = 'ABCDEFGHIJKL'
    subNotatedSlots = 'ABCDEFGHIJKLMNO'
    slots = [
        annotatedSlots,
        mid1Slots,
        mid2Slots,
        mid3Slots,
        subNotatedSlots
    ]
    classes = [AnnotatedClass, MidNote1, MidNote2, MidNote3, SubNotated]
    for slot, cls in zip(slots, classes):
      print(77 * '_')
      print(cls.__name__)
      print(slot, )
      print(cls.__slots__)
      print(77 * '¨')

  def test_annotated_good_get(self) -> None:
    """
    Test that EZData classes with annotated slots can be instantiated and
    accessed correctly.
    """
