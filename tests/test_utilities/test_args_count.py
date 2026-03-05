"""
The 'testArgsCount' module tests the 'argsCount' utility function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import argsCount, textFmt

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Foo:

  @staticmethod
  def noArgs() -> Any:
    return ()

  @classmethod
  def boundOnly(cls) -> Any:
    return (cls,)

  def oneArg(self: Any = 'self', arg1: Any = 'arg1') -> Any:
    return (self, arg1)

  def twoArgs(
      self: Any = 'self',
      arg1: Any = 'arg1',
      arg2: Any = 'arg2',
      ) -> Any:
    return (self, arg1, arg2)


class TestArgsCount(UtilitiesTest):

  def setUp(self, ) -> None:
    super().setUp()
    self.foo = Foo()
    self.funcs = (
      Foo.noArgs,
      Foo.boundOnly,
      Foo.oneArg,
      Foo.twoArgs,
      self.foo.noArgs,
      self.foo.boundOnly,
      self.foo.oneArg,
      self.foo.twoArgs,
      )

  def test_dev_null(self) -> None:
    self.assertTrue(True)

  def test_count(self, ) -> None:
    for func in self.funcs:
      left = func()
      right = argsCount(func)
      self.assertEqual(right, len(left))
