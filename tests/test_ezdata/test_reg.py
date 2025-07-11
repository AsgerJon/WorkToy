"""
TestReg tests the regularly defined EZData classes. That is, where slots
are defined by setting class variables directly, without using type hints.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZTest, RegularClass, Mid1, Mid2, Mid3, SubClass

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestReg(EZTest):
  """
  TestInit tests that EZData classes correctly initialize.
  """

  def test_base_get_good(self) -> None:
    """Testing 'get' on the base class without inheritance."""
    ez = RegularClass()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    ez = RegularClass(69, 420, 1337)
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)

  def test_base_set_good(self) -> None:
    """Testing 'set' on the base class without inheritance."""
    ez = RegularClass()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)

  def test_mid1_get_good(self) -> None:
    """Testing 'get' on the first mid-level class."""
    ez = Mid1()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)

  def test_mid1_set_good(self) -> None:
    """Testing 'set' on the first mid-level class."""
    ez = Mid1()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
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

  def test_mid2_get_good(self) -> None:
    """Testing 'get' on the second mid-level class."""
    ez = Mid2()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
    self.assertEqual(ez.g, 60)
    self.assertEqual(ez.h, 70)
    self.assertEqual(ez.i, 80)

  def test_mid2_set_good(self) -> None:
    """Testing 'set' on the second mid-level class."""
    ez = Mid2()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
    self.assertEqual(ez.g, 60)
    self.assertEqual(ez.h, 70)
    self.assertEqual(ez.i, 80)
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

  def test_mid3_get_good(self) -> None:
    """Testing 'get' on the third mid-level class."""
    ez = Mid3()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
    self.assertEqual(ez.g, 60)
    self.assertEqual(ez.h, 70)
    self.assertEqual(ez.i, 80)
    self.assertEqual(ez.j, 90)
    self.assertEqual(ez.k, 100)
    self.assertEqual(ez.l, 110)

  def test_mid3_set_good(self) -> None:
    """Testing 'set' on the third mid-level class."""
    ez = Mid3()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
    self.assertEqual(ez.g, 60)
    self.assertEqual(ez.h, 70)
    self.assertEqual(ez.i, 80)
    self.assertEqual(ez.j, 90)
    self.assertEqual(ez.k, 100)
    self.assertEqual(ez.l, 110)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    ez.d = 80085
    ez.e = 8008135
    ez.f = 69
    ez.g = 420
    ez.h = 1337
    ez.i = 80085
    ez.j = 69
    ez.k = 420
    ez.l = 1337
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)
    self.assertEqual(ez.g, 420)
    self.assertEqual(ez.h, 1337)
    self.assertEqual(ez.i, 80085)
    self.assertEqual(ez.j, 69)
    self.assertEqual(ez.k, 420)
    self.assertEqual(ez.l, 1337)

  def test_subclass_get_good(self) -> None:
    """Testing 'get' on the subclass."""
    ez = SubClass()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
    self.assertEqual(ez.g, 60)
    self.assertEqual(ez.h, 70)
    self.assertEqual(ez.i, 80)
    self.assertEqual(ez.j, 90)
    self.assertEqual(ez.k, 100)
    self.assertEqual(ez.l, 110)
    self.assertEqual(ez.m, 120)
    self.assertEqual(ez.n, 130)
    self.assertEqual(ez.o, 140)

  def test_subclass_set_good(self) -> None:
    """Testing 'set' on the subclass."""
    ez = SubClass()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    self.assertEqual(ez.d, 30)
    self.assertEqual(ez.e, 40)
    self.assertEqual(ez.f, 50)
    self.assertEqual(ez.g, 60)
    self.assertEqual(ez.h, 70)
    self.assertEqual(ez.i, 80)
    self.assertEqual(ez.j, 90)
    self.assertEqual(ez.k, 100)
    self.assertEqual(ez.l, 110)
    self.assertEqual(ez.m, 120)
    self.assertEqual(ez.n, 130)
    self.assertEqual(ez.o, 140)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    ez.d = 80085
    ez.e = 8008135
    ez.f = 69
    ez.g = 420
    ez.h = 1337
    ez.i = 80085
    ez.j = 69
    ez.k = 420
    ez.l = 1337
    ez.m = 80085
    ez.n = 8008135
    ez.o = 69
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)
    self.assertEqual(ez.d, 80085)
    self.assertEqual(ez.e, 8008135)
    self.assertEqual(ez.f, 69)
    self.assertEqual(ez.g, 420)
    self.assertEqual(ez.h, 1337)
    self.assertEqual(ez.i, 80085)
    self.assertEqual(ez.j, 69)
    self.assertEqual(ez.k, 420)
    self.assertEqual(ez.l, 1337)
    self.assertEqual(ez.m, 80085)
    self.assertEqual(ez.n, 8008135)
    self.assertEqual(ez.o, 69)
