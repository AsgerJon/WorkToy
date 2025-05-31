"""
TestBaseOverload tests the most basic overload functionalities
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject
from worktoy.static import Dispatch, overload
from worktoy.static.zeroton import THIS

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class Foo(BaseObject):
  """
  Foo is overloaded
  """

  calledTypes = None

  @overload(int)
  def __init__(self, *args) -> None:
    setattr(self, 'calledTypes', int)

  @overload(str)
  def __init__(self, *args) -> None:
    setattr(self, 'calledTypes', str)

  @overload(int, int)
  def __init__(self, *args) -> None:
    setattr(self, 'calledTypes', (int, int))

  @overload(THIS)
  def __init__(self, *args) -> None:
    """
    This is the default constructor.
    """
    setattr(self, 'calledTypes', THIS)


class Bar(BaseObject):
  """
  Bar is overloaded
  """

  calledTypes = None

  @overload(float, )
  def __init__(self, *args) -> None:
    """Initialize Bar with a float."""
    setattr(self, 'calledTypes', 1)

  @overload(float, float)
  def __init__(self, *args) -> None:
    """Initialize Bar with a complex number."""
    setattr(self, 'calledTypes', 2)

  @overload(float, float, float)
  def __init__(self, *args) -> None:
    """Initialize Bar with a complex number."""
    setattr(self, 'calledTypes', 3)


class TestBaseOverload(TestCase):
  """TestBaseOverload tests the most basic overload functionalities."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.strFoo = Foo('69')
    self.intFoo = Foo(69)
    self.intIntFoo = Foo(69, 420)
    self.thisFoo = Foo(self.strFoo)
    #  Fast
    self.float1Bar = Bar(0.1337)
    self.float2Bar = Bar(0.1337, 0.80085)
    self.float3Bar = Bar(0.1337, 0.80085, -69.69)
    #  Cast
    self.int1Bar = Bar(69)
    self.int2Bar = Bar(69, 420)
    self.int3Bar = Bar(69, 420, 1337)

  def test_ad_hoc(self, ) -> None:
    """Test ad-hoc dispatching."""
    self.assertTrue(True)

  def test_init(self, ) -> None:
    """
    Tests that the correct __init__ is called.
    """
    self.assertIsInstance(self.strFoo, Foo)
    self.assertIsInstance(self.intFoo, Foo)
    self.assertIsInstance(self.intIntFoo, Foo)
    self.assertIsInstance(self.thisFoo, Foo)

    self.assertIsInstance(self.float1Bar, Bar)
    self.assertIsInstance(self.float2Bar, Bar)
    self.assertIsInstance(self.float3Bar, Bar)
    self.assertIsInstance(self.int1Bar, Bar)
    self.assertIsInstance(self.int2Bar, Bar)
    self.assertIsInstance(self.int3Bar, Bar)

  def test_attr(self, ) -> None:
    """
    Tests the attributes on the class itself
    """
    self.assertIsInstance(Foo.__init__, Dispatch)

  def test_fast(self, ) -> None:
    """
    Tests that the correct dispatches are called.
    """
    self.assertEqual(self.strFoo.calledTypes, str)
    self.assertEqual(self.intFoo.calledTypes, int)
    self.assertIsInstance(self.intIntFoo.calledTypes, tuple)
    self.assertEqual(self.intIntFoo.calledTypes, (int, int))
    self.assertIs(self.thisFoo.calledTypes, THIS)

    self.assertEqual(self.float1Bar.calledTypes, 1)
    self.assertEqual(self.float2Bar.calledTypes, 2)
    self.assertEqual(self.float3Bar.calledTypes, 3)

  def test_cast(self) -> None:
    """
    Tests that the cast works correctly.
    """

    self.assertEqual(self.int1Bar.calledTypes, 1)
    self.assertEqual(self.int2Bar.calledTypes, 2)
    self.assertEqual(self.int3Bar.calledTypes, 3)
