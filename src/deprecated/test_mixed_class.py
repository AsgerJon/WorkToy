"""
TestMixedClass tests EZData classes that mixes between regular slots and
slots set as type hints.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZTest, Mix1, Mix2, Mix3, MixedSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestMixedClass(EZTest):
  """
  TestMixedClass tests EZData classes that mixes between regular slots and
  slots set as type hints.
  """

  def test_mix1_get_good(self) -> None:
    """Testing 'get' on the first mixed class."""
    ez = Mix1()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    ez = Mix1(69, 420, 1337)
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)

  def test_mix1_set_good(self) -> None:
    """Testing 'set' on the first mixed class."""
    ez = Mix1()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)

  def test_mix2_get_good(self) -> None:
    """Testing 'get' on the second mixed class."""
    ez = Mix2()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    self.assertEqual(ez.d, 0)
    self.assertEqual(ez.e, 0)
    self.assertEqual(ez.f, 0)
    ez = Mix2(69, 420, 1337, 80085, 8008135, 69)
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)

  def test_mix2_set_good(self) -> None:
    """Testing 'set' on the second mixed class."""
    ez = Mix2()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    self.assertEqual(ez.d, 0)
    self.assertEqual(ez.e, 0)
    self.assertEqual(ez.f, 0)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    ez.d = 80085
    ez.e = 8008135
    ez.f = 69
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)

  def test_mix3_get_good(self) -> None:
    """Testing 'get' on the third mixed class."""
    ez = Mix3()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    self.assertEqual(ez.d, 0)
    self.assertEqual(ez.e, 0)
    self.assertEqual(ez.f, 0)
    self.assertEqual(ez.g, 0)
    self.assertEqual(ez.h, 0)
    self.assertEqual(ez.i, 0)
    ez = Mix3(69, 420, 1337, 80085, 8008135, 69, 420, 1337, 80085)
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)
    self.assertEqual(ez.g, 420)
    self.assertEqual(ez.h, 1337)
    self.assertEqual(ez.i, 80085)

  def test_mix3_set_good(self) -> None:
    """Testing 'set' on the third mixed class."""
    ez = Mix3()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    self.assertEqual(ez.d, 0)
    self.assertEqual(ez.e, 0)
    self.assertEqual(ez.f, 0)
    self.assertEqual(ez.g, 0)
    self.assertEqual(ez.h, 0)
    self.assertEqual(ez.i, 0)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    ez.d = 80085
    ez.e = 8008135
    ez.f = 69
    ez.g = 420
    ez.h = 1337
    ez.i = 80085
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)
    self.assertEqual(ez.g, 420)
    self.assertEqual(ez.h, 1337)
    self.assertEqual(ez.i, 80085)

  def test_mixed_slot_get_good(self) -> None:
    """Testing 'get' on the mixed slot class."""
    ez = MixedSlot()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    self.assertEqual(ez.d, 0)
    self.assertEqual(ez.e, 0)
    self.assertEqual(ez.f, 0)
    self.assertEqual(ez.g, 0)
    self.assertEqual(ez.h, 0)
    self.assertEqual(ez.i, 0)
    self.assertEqual(ez.j, 0)
    ez = MixedSlot(69,
                   420,
                   1337,
                   80085,
                   8008135,
                   69,
                   420,
                   1337,
                   80085,
                   8008135)
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)
    self.assertEqual(ez.g, 420)
    self.assertEqual(ez.h, 1337)
    self.assertEqual(ez.i, 80085)
    self.assertEqual(ez.j, 8008135)

  def test_mixed_slot_set_good(self) -> None:
    """Testing 'set' on the mixed slot class."""
    ez = MixedSlot()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 0)
    self.assertEqual(ez.c, 0)
    self.assertEqual(ez.d, 0)
    self.assertEqual(ez.e, 0)
    self.assertEqual(ez.f, 0)
    self.assertEqual(ez.g, 0)
    self.assertEqual(ez.h, 0)
    self.assertEqual(ez.i, 0)
    self.assertEqual(ez.j, 0)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    ez.d = 80085
    ez.e = 8008135
    ez.f = 69
    ez.g = 420
    ez.h = 1337
    ez.i = 80085
    ez.j = 8008135
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)
    self.assertEqual(ez.g, 420)
    self.assertEqual(ez.h, 1337)
    self.assertEqual(ez.i, 80085)
    self.assertEqual(ez.j, 8008135)
