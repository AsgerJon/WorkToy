"""TestOverFunc - Test the OverFunc class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import OverloadedFunction as OverFunc, TypeSig
from worktoy.static import overload


def func() -> None: pass


Func = type(func)


class Foo:
  """Helper class for testing."""

  @overload.fallback
  def bar(self, *args) -> str:
    """Overloaded function."""
    pass

  @overload(int, int)
  @overload(float, float)
  def bar2(self, *args) -> str:
    """Overloaded function."""
    pass


class TestOverFunc(TestCase):
  """Test the OverFunc class."""

  def setUp(self, ) -> None:
    """Set up the test."""
    self.foo = Foo()

  def test_overload(self, ) -> None:
    """Test the overload function."""
    self.assertIsInstance(self.foo.bar, OverFunc)
    self.assertIsInstance(self.foo.bar2, OverFunc)

  def test_fallback_flag(self, ) -> None:
    """Tests the fallback flag."""
    self.assertTrue(self.foo.bar.isFallback)
    self.assertFalse(self.foo.bar2.isFallback)

  def test_has_func(self, ) -> None:
    """Test the hasFunc function."""
    self.assertIsInstance(self.foo.bar.getFunc(), Func)
    self.assertIsInstance(self.foo.bar2.getFunc(), Func)

  def test_func_name(self, ) -> None:
    """Test the funcName function."""
    self.assertEqual(self.foo.bar.getFunc().__name__, 'bar')
    self.assertEqual(self.foo.bar2.getFunc().__name__, 'bar2')

  def test_type_sigs(self, ) -> None:
    """Test the typeSigs function."""
    for oFunc in [self.foo.bar, self.foo.bar2]:
      for sig in oFunc.getTypeSigs():
        self.assertIsInstance(sig, TypeSig)
    self.assertEqual(len(self.foo.bar.getTypeSigs()), 1)
    self.assertEqual(len(self.foo.bar2.getTypeSigs()), 2)
