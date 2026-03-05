"""
TestTakesKwargs tests the 'worktoy.utilities.takesKwargs' function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import takesKwargs

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Foo:

  def acceptsKwargs1(self, **kwargs: Any) -> bool:
    return True

  def rejectsKwargs1(self, arg1: Any) -> bool:
    return False


class TestTakesKwargs(UtilitiesTest):
  """
  TestTakesKwargs tests the 'worktoy.utilities.takesKwargs' function.
  """

  def test_kwargs_flag(self, ) -> None:
    """
    Tests the 'takesKwargs' function by defining two methods, one that
    accepts kwargs and one that does not, and asserting that 'takesKwargs'
    returns 'True' for the former and 'False' for the latter.
    """

    self.assertTrue(Foo().acceptsKwargs1())
    self.assertTrue(takesKwargs(Foo.acceptsKwargs1))
    self.assertFalse(Foo().rejectsKwargs1(object()))
    self.assertFalse(takesKwargs(Foo.rejectsKwargs1))
