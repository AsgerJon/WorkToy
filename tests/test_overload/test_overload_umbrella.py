"""
TestOverloadUmbrella covers obscure edge cases and esoteric fallbacks of the
overload system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import THIS
from worktoy.mcls import BaseObject
from worktoy.static import overload

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Any


class Foo(BaseObject):
  """Foo implements neither __overload_eq__ nor __overload_ne__."""

  __fallback_value__ = None
  __inner_value__ = None
  __instance_name__ = None

  @overload(THIS, str)
  def __init__(self, other: Self, name: str):
    self.__inner_value__ = other.__inner_value__
    self.__instance_name__ = name

  @overload(int, str)
  def __init__(self, other: int, name: str):
    self.__inner_value__ = other
    self.__instance_name__ = name


class TestOverloadUmbrella(TestCase):
  """
  TestOverloadUmbrella covers obscure edge cases and esoteric fallbacks of
  the
  overload system.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def setUp(self) -> None:
    self.foo = Foo(69, '420')

  def testOverloadSelfName(self) -> None:
    """
    Test that the overload system correctly handles self-naming.
    """
    self.assertEqual(self.foo.__instance_name__, '420')
    self.assertEqual(self.foo.__inner_value__, 69)
    bar = Foo(self.foo, '1337')
    self.assertEqual(bar.__instance_name__, '1337')
    self.assertEqual(bar.__inner_value__, 69)

  def testFlexNameInt(self) -> None:
    """
    Test that the overload system correctly handles int naming.
    """
    foo = Foo('breh', 80085)
    self.assertEqual(foo.__instance_name__, 'breh')
    self.assertEqual(foo.__inner_value__, 80085)

  def testInitName(self) -> None:
    """
    Test that the overload system correctly handles init naming.
    """
    self.assertEqual(Foo.__init__.__name__, '__init__')
    self.assertEqual(Foo.__init__.__qualname__, 'Foo.__init__')

  def testDerpName(self, ) -> None:
    """
    Test that the overload system correctly handles derp naming.
    """
    with self.assertRaises(AttributeError) as context:
      _ = Foo.__init__.urmom
    e = context.exception
    expected = 'has no attribute'
    self.assertIn(expected, str(e))
