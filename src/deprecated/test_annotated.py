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
      for expected, actual in zip(slot, cls.__slots__):
        self.assertEqual(expected, actual, )

  def test_annotated_good_get(self) -> None:
    """
    Test that EZData classes with annotated slots can be instantiated and
    accessed correctly.
    """
    ez = AnnotatedClass()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    ez = AnnotatedClass(69, 420, 1337)
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)

  def test_annotated_good_set(self) -> None:
    """
    Test that EZData classes with annotated slots can be set correctly.
    """
    ez = AnnotatedClass()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    ez.A = 69
    ez.B = 420
    ez.C = 1337
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)

  def test_mid1_annotated_good_get(self) -> None:
    """
    Test that the first mid-level class with annotated slots can be
    instantiated and accessed correctly.
    """
    ez = MidNote1()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    ez = MidNote1(69, 420, 1337, 80085, 8008135, 69)
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)

  def test_mid1_annotated_good_set(self) -> None:
    """
    Test that the first mid-level class with annotated slots can be set
    correctly.
    """
    ez = MidNote1()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    ez.A = 69
    ez.B = 420
    ez.C = 1337
    ez.D = 80085
    ez.E = 8008135
    ez.F = 69
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)

  def test_mid2_annotated_good_get(self) -> None:
    """
    Test that the second mid-level class with annotated slots can be
    instantiated and accessed correctly.
    """
    ez = MidNote2()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    self.assertEqual(ez.G, 0)
    self.assertEqual(ez.H, 0)
    self.assertEqual(ez.I, 0)
    ez = MidNote2(69, 420, 1337, 80085, 8008135, 69, 1234, 5678, 91011)
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)
    self.assertEqual(ez.G, 1234)
    self.assertEqual(ez.H, 5678)
    self.assertEqual(ez.I, 91011)

  def test_mid2_annotated_good_set(self) -> None:
    """
    Test that the second mid-level class with annotated slots can be set
    correctly.
    """
    ez = MidNote2()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    self.assertEqual(ez.G, 0)
    self.assertEqual(ez.H, 0)
    self.assertEqual(ez.I, 0)
    ez.A = 69
    ez.B = 420
    ez.C = 1337
    ez.D = 80085
    ez.E = 8008135
    ez.F = 69
    ez.G = 420
    ez.H = 1337
    ez.I = 80085
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)
    self.assertEqual(ez.G, 420)
    self.assertEqual(ez.H, 1337)
    self.assertEqual(ez.I, 80085)

  def test_mid3_annotated_good_get(self) -> None:
    """
    Test that the third mid-level class with annotated slots can be
    instantiated and accessed correctly.
    """
    ez = MidNote3()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    self.assertEqual(ez.G, 0)
    self.assertEqual(ez.H, 0)
    self.assertEqual(ez.I, 0)
    self.assertEqual(ez.J, 0)
    self.assertEqual(ez.K, 0)
    self.assertEqual(ez.L, 0)
    ez = MidNote3(69, 420, 1337, 80085, 8008135, 69,
                  420, 1337, 80085, 8008135, 69, 420)
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)
    self.assertEqual(ez.G, 420)
    self.assertEqual(ez.H, 1337)
    self.assertEqual(ez.I, 80085)
    self.assertEqual(ez.J, 8008135)
    self.assertEqual(ez.K, 69)
    self.assertEqual(ez.L, 420)

  def test_mid3_annotated_good_set(self) -> None:
    """
    Test that the third mid-level class with annotated slots can be set
    correctly.
    """
    ez = MidNote3()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    self.assertEqual(ez.G, 0)
    self.assertEqual(ez.H, 0)
    self.assertEqual(ez.I, 0)
    self.assertEqual(ez.J, 0)
    self.assertEqual(ez.K, 0)
    self.assertEqual(ez.L, 0)
    ez.A = 69
    ez.B = 420
    ez.C = 1337
    ez.D = 80085
    ez.E = 8008135
    ez.F = 69
    ez.G = 420
    ez.H = 1337
    ez.I = 80085
    ez.J = 8008135
    ez.K = 69
    ez.L = 420
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)
    self.assertEqual(ez.G, 420)
    self.assertEqual(ez.H, 1337)
    self.assertEqual(ez.I, 80085)
    self.assertEqual(ez.J, 8008135)
    self.assertEqual(ez.K, 69)
    self.assertEqual(ez.L, 420)

  def test_sub_notated_annotated_good_get(self) -> None:
    """
    Test that the sub-notated class with annotated slots can be
    instantiated and accessed correctly.
    """
    ez = SubNotated()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    self.assertEqual(ez.G, 0)
    self.assertEqual(ez.H, 0)
    self.assertEqual(ez.I, 0)
    self.assertEqual(ez.J, 0)
    self.assertEqual(ez.K, 0)
    self.assertEqual(ez.L, 0)
    self.assertEqual(ez.M, 0)
    self.assertEqual(ez.N, 0)
    self.assertEqual(ez.O, 0)
    ez = SubNotated(69, 420, 1337, 80085, 8008135,
                    69, 420, 1337, 80085, 8008135,
                    69, 420, 1337, 80085, 8008135,
                    69)
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)
    self.assertEqual(ez.G, 420)
    self.assertEqual(ez.H, 1337)
    self.assertEqual(ez.I, 80085)
    self.assertEqual(ez.J, 8008135)
    self.assertEqual(ez.K, 69)
    self.assertEqual(ez.L, 420)
    self.assertEqual(ez.M, 1337)
    self.assertEqual(ez.N, 80085)
    self.assertEqual(ez.O, 8008135)

  def test_sub_notated_annotated_good_set(self) -> None:
    """
    Test that the sub-notated class with annotated slots can be set
    correctly.
    """
    ez = SubNotated()
    self.assertEqual(ez.A, 0)
    self.assertEqual(ez.B, 0)
    self.assertEqual(ez.C, 0)
    self.assertEqual(ez.D, 0)
    self.assertEqual(ez.E, 0)
    self.assertEqual(ez.F, 0)
    self.assertEqual(ez.G, 0)
    self.assertEqual(ez.H, 0)
    self.assertEqual(ez.I, 0)
    self.assertEqual(ez.J, 0)
    self.assertEqual(ez.K, 0)
    self.assertEqual(ez.L, 0)
    self.assertEqual(ez.M, 0)
    self.assertEqual(ez.N, 0)
    self.assertEqual(ez.O, 0)
    ez.A = 69
    ez.B = 420
    ez.C = 1337
    ez.D = 80085
    ez.E = 8008135
    ez.F = 69
    ez.G = 420
    ez.H = 1337
    ez.I = 80085
    ez.J = 8008135
    ez.K = 69
    ez.L = 420
    ez.M = 1337
    ez.N = 80085
    ez.O = 8008135
    self.assertEqual(ez.A, 69)
    self.assertEqual(ez.B, 420)
    self.assertEqual(ez.C, 1337)
    self.assertEqual(ez.D, 80085)
    self.assertEqual(ez.E, 8008135)
    self.assertEqual(ez.F, 69)
    self.assertEqual(ez.G, 420)
    self.assertEqual(ez.H, 1337)
    self.assertEqual(ez.I, 80085)
    self.assertEqual(ez.J, 8008135)
    self.assertEqual(ez.K, 69)
    self.assertEqual(ez.L, 420)
    self.assertEqual(ez.M, 1337)
    self.assertEqual(ez.N, 80085)
    self.assertEqual(ez.O, 8008135)
