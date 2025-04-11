"""TestDispatch tests the Dispatch class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractNamespace, AbstractMetaclass
from worktoy.parse import maybe
from worktoy.static import OverloadedFunction as OverFunc, TypeSig
from worktoy.static import overload

from worktoy.static import Dispatch


class FooSpace(AbstractNamespace):
  """Helper class for testing."""

  __over_funcs__ = None

  def getOverFuncs(self, **kwargs) -> dict[str, list[OverFunc]]:
    """Get the overloaded functions."""
    return maybe(self.__over_funcs__, {})

  def _addOverFunc(self, key: str, overFunc: OverFunc) -> None:
    """Add an overloaded function to the overload space."""
    overFuncs = self.getOverFuncs()
    existing = overFuncs.get(key, [])
    overFuncs[key] = [*existing, overFunc]
    self.__over_funcs__ = overFuncs

  def _collectOverFuncs(self, ) -> None:
    """Collect the overloaded functions."""
    for key, funcs in self.getOverFuncs().items():
      AbstractNamespace.__setitem__(self, key, Dispatch(*funcs))

  def __setitem__(self, key: str, value: OverFunc) -> None:
    """Set the item."""
    if isinstance(value, OverFunc):
      return self._addOverFunc(key, value)
    AbstractNamespace.__setitem__(self, key, value)

  def compile(self, ) -> dict:
    """Compile the namespace."""
    self._collectOverFuncs()
    return AbstractNamespace.compile(self)


class FooMeta(AbstractMetaclass):
  """Helper class for testing."""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> FooSpace:
    """Prepare the class namespace."""
    return FooSpace(mcls, name, bases, **kwargs)


class Foo(metaclass=FooMeta):
  """Helper class for testing."""

  @overload.fallback
  def bar(self, *args) -> str:
    """Overloaded function."""
    return 'Fallback'

  @overload(int, int)
  @overload(float, float)
  def bar(self, *args) -> str:
    """Overloaded function."""
    return 'int, int or float, float'

  @overload(int, int)
  @overload(float, float)
  def bar2(self, *args) -> str:
    """Overloaded function."""
    return 'int, int or float, float'

  @overload(str, str)
  def bar2(self, *args) -> str:
    """Overloaded function."""
    return 'str, str'


class TestDispatch(TestCase):
  """Test the Dispatch class."""

  def setUp(self, ) -> None:
    """Set up the test."""
    self.foo = Foo()

  def test_is_dispatch(self, ) -> None:
    """Test the isDispatch function."""
    self.assertIsInstance(self.foo.bar, Dispatch)
    self.assertIsInstance(self.foo.bar2, Dispatch)

  def test_names(self, ) -> None:
    """Test the names"""
    self.assertEqual(self.foo.bar.__name__, 'bar')
    self.assertEqual(self.foo.bar2.__name__, 'bar2')

  def test_has_fallback(self, ) -> None:
    """Test the hasFallback function."""
    self.assertTrue(self.foo.bar.hasFallback)
    self.assertFalse(self.foo.bar2.hasFallback)

  def test_bound_instance(self, ) -> None:
    """Test the bound instance"""
    self.assertIs(self.foo.bar.__bound_instance__, self.foo)
    self.assertIs(self.foo.bar2.__bound_instance__, self.foo)

  def test_calls(self, ) -> None:
    """Tests that the calls are correct."""
    intFloat = 'int, int or float, float'
    fallback = 'Fallback'
    strStr = 'str, str'
    self.assertEqual(self.foo.bar(69, 420), intFloat)
    self.assertEqual(self.foo.bar(1337., 80085.), intFloat)
    self.assertEqual(self.foo.bar('breh'), fallback)
    self.assertEqual(self.foo.bar2(69, 420), intFloat)
    self.assertEqual(self.foo.bar2(1337., 80085.), intFloat)
    self.assertEqual(self.foo.bar2('always', 'test!'), strStr)
