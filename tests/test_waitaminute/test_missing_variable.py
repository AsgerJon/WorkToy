"""
TestMissingVariable tests the custom exception class 'MissingVariable'
from the 'worktoy.waitaminute' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.waitaminute import MissingVariable
from . import WaitAMinuteTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Foo:
  """Test class having variable 'bar'. """

  __bar_value__ = None

  bar = Field()

  @bar.GET
  def _getBarValue(self) -> Any:
    if self.__bar_value__ is None:
      raise MissingVariable(self, 'bar', object)
    return self.__bar_value__

  def __init__(self, *args) -> None:
    if args:
      self.__bar_value__ = args[0]


class TestMissingVariable(WaitAMinuteTest):
  """
  TestMissingVariable tests the custom exception class 'MissingVariable'
  from the 'worktoy.waitaminute' package.
  """

  def testFoo(self) -> None:
    """Testing that the Foo class functions"""

    foo1 = Foo()  # No value set for 'bar'
    foo2 = Foo(69)

    self.assertIsInstance(foo1, Foo)
    self.assertIsInstance(foo2, Foo)
    self.assertIsNone(foo1.__bar_value__)
    self.assertEqual(foo2.__bar_value__, 69)
    self.assertEqual(foo2.bar, 69)

  def testRaises(self) -> None:
    """Testing that the MissingVariable exception is raised correctly"""
    foo = Foo()
    with self.assertRaises(MissingVariable) as context:
      _ = foo.bar
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertEqual(e.name, 'bar')
    self.assertIs(e.type_, object)
    self.assertEqual(str(e), repr(e))
