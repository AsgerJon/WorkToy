"""
TestOverloadFunc tests the special case where a type signature used in an
overload consists of a function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import types
from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Callable


class Foo(BaseObject):
  @overload(int)
  def __init__(self, value: int) -> None:
    self.value = value

  @overload(types.FunctionType)
  def __init__(self, func: Callable) -> None:
    self.value = func()


class TestOverloadFunc(OverloadTest):
  """
  TestOverloadFunc tests the special case where a type signature used in an
  overload consists of a function.
  """

  def test_overload_func(self) -> Self:
    """Tests the overload with a function type signature."""

    def sampleFunc():
      return 42

    foo1 = Foo(10)
    self.assertEqual(foo1.value, 10)

    foo2 = Foo(sampleFunc)
    self.assertEqual(foo2.value, 42)
