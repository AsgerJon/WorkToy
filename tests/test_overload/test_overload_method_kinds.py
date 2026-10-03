"""
TestOverloadMethodKinds subclasses 'OverloadTest' and pins that
'overload', 'overload.fallback' and 'overload.finalize' refuse a
staticmethod and a classmethod with 'TypeException' at the decorator.
The 'Dispatcher' they build calls every function with the instance
first, so either kind used to build the class and fail at the first
call, the staticmethod receiving the instance as its first argument.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.waitaminute import TypeException

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _plain(*args) -> tuple:
  return args  # pragma: no cover


class TestOverloadMethodKinds(OverloadTest):
  """
  TestOverloadMethodKinds provides tests for overloading a staticmethod
  or a classmethod.
  """

  def test_overload_refuses(self) -> None:
    """'overload' refuses both kinds, naming 'func'."""
    for kind in (staticmethod, classmethod):
      with self.subTest(kind=kind):
        with self.assertRaises(TypeException) as context:
          overload(int)(kind(_plain))
        self.assertEqual(context.exception.varName, 'func')

  def test_stacked_overload_refuses(self) -> None:
    """A further 'overload' stacked over the refused kind is never
    reached, since the first decorator raises."""
    with self.assertRaises(TypeException):
      overload(str)(overload(int)(staticmethod(_plain)))

  def test_fallback_and_finalize_refuse(self) -> None:
    """'overload.fallback' and 'overload.finalize' refuse both kinds."""
    for decorator in (overload.fallback, overload.finalize):
      for kind in (staticmethod, classmethod):
        with self.subTest(decorator=decorator, kind=kind):
          with self.assertRaises(TypeException):
            decorator(kind(_plain))

  def test_plain_function_accepted(self) -> None:
    """A plain function is accepted by each."""
    self.assertIsInstance(overload(int)(_plain), overload)
    self.assertIsInstance(overload.fallback(_plain), overload)
    self.assertIsInstance(overload.finalize(_plain), overload)
