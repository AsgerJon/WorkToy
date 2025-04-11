"""TestOverloadMeta tests the OverloadMeta class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import OverloadedFunction as OverFunc, Dispatch
from worktoy.static import overload, TypeSig

from worktoy.mcls import AbstractNamespace, AbstractMetaclass
from worktoy.mcls import OverloadSpace as OSpace
from worktoy.mcls import OverloadMeta as OMeta
from worktoy.waitaminute import DispatchException


# class Breh(metaclass=OMeta, trustMeBro=True):
#   """Testing implicit calls to the namespace"""


class Foo(metaclass=OMeta):
  """Helper class for testing."""

  __fallback_bar3__ = 'The flex function could not parse the arguments!'

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

  @overload(str, str)
  def bar3(self, *args) -> str:
    """Overloaded function."""
    num, word = [*args, None, None][:2]
    return """Number: %s, Word: %s""" % (num, word)

  @overload.fallback(int, str)
  def bar3(self, *args) -> str:
    """Overloaded function."""
    num, word = None, None
    for arg in args:
      if isinstance(arg, int) and num is None:
        num = arg
      elif isinstance(arg, str) and word is None:
        word = arg
      if num is None or word is None:
        continue
      break
    else:
      return self.__fallback_bar3__
    return """Number: %s, Word: %s""" % (num, word)

  @overload.flex(int, int, int)
  def bar4(self, *args) -> str:
    """Flexible function."""
    intArgs = [arg for arg in args if isinstance(arg, int)]
    return '(%s)' % ', '.join(['%d' % arg for arg in intArgs])


class TestDispatch(TestCase):
  """Test the Dispatch class."""

  def setUp(self, ) -> None:
    """Set up the test."""
    self.foo = Foo()

  def test_is_dispatch(self, ) -> None:
    """Test the isDispatch function."""
    self.assertIsInstance(self.foo.bar, Dispatch)
    self.assertIsInstance(self.foo.bar2, Dispatch)
    self.assertIsInstance(self.foo.bar3, Dispatch)

  def test_names(self, ) -> None:
    """Test the names"""
    self.assertEqual(self.foo.bar.__name__, 'bar')
    self.assertEqual(self.foo.bar2.__name__, 'bar2')
    self.assertEqual(self.foo.bar3.__name__, 'bar3')

  def test_has_fallback(self, ) -> None:
    """Test the hasFallback function."""
    self.assertTrue(self.foo.bar.hasFallback)
    self.assertFalse(self.foo.bar2.hasFallback)
    self.assertTrue(self.foo.bar3.hasFallback)
    self.assertFalse(self.foo.bar4.hasFallback)

  def test_has_flex(self, ) -> None:
    """Test the hasFlex function."""
    self.assertFalse(self.foo.bar.hasFlex)
    self.assertFalse(self.foo.bar2.hasFlex)
    self.assertFalse(self.foo.bar3.hasFlex)
    self.assertTrue(self.foo.bar4.hasFlex)

  def test_bound_instance(self, ) -> None:
    """Test the bound instance"""
    self.assertIs(self.foo.bar.__bound_instance__, self.foo)
    self.assertIs(self.foo.bar2.__bound_instance__, self.foo)
    self.assertIs(self.foo.bar3.__bound_instance__, self.foo)
    self.assertIs(self.foo.bar4.__bound_instance__, self.foo)

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
    self.assertEqual(self.foo.bar3('69', 'test'), 'Number: 69, Word: test')
    self.assertEqual(self.foo.bar3('test', 69), 'Number: test, Word: 69')
    self.assertEqual(self.foo.bar3('test'), self.foo.__fallback_bar3__)

  def test_flex(self, ) -> None:
    """Tests that the flex function works."""
    expected = '(69, 420, 1337)'
    intFloatInt = (69, 420.0, 1337)
    intFloatStr = (69, 420.0, '1337')
    intFloatMix = (69, 420.0, '1337', 80085)

    self.assertEqual(self.foo.bar4(*intFloatInt), expected)
    self.assertEqual(self.foo.bar4(*intFloatStr), expected)
    self.assertEqual(self.foo.bar4(*intFloatMix), expected)

  def test_errors(self, ) -> None:
    """Tests that the errors are correct."""
    with self.assertRaises(DispatchException):
      self.foo.bar2()  # Too few arguments
    with self.assertRaises(DispatchException):
      self.foo.bar4()  # Too few arguments
