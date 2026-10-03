"""
TestCastBuiltinSubclass subclasses 'DispatcherTest' and pins what the
cast passes of a 'Dispatcher' do with a signature over a subclass of a
builtin. A subclass that keeps the constructor of its builtin is reached
through a cast only with a value the builtin's rule accepts, and the
overload then receives an instance of the subclass; a value the rule
refuses goes on to the fallback, where it used to reach the overload
rounded, as '2' for '2.5'. A subclass with a constructor of its own is
trusted, and its constructor decides, as it does for an 'AttriBox'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestCastBuiltinSubclass(DispatcherTest):
  """
  TestCastBuiltinSubclass provides tests for the cast passes of a
  'Dispatcher' and signatures over subclasses of the builtins.
  """

  def test_subclass_signature(self) -> None:
    """'2.5' reaches the fallback, while '2.0' reaches the overload as an
    instance of the subclass."""

    class MyInt(int):
      pass

    class Router(BaseObject):
      @overload(MyInt)
      def route(self, value: Any) -> Any:
        return 'MyInt', type(value), value

      @overload.fallback
      def route(self, *args: Any) -> Any:
        return 'fallback', args

    router = Router()
    self.assertEqual(router.route(2.5), ('fallback', (2.5,)))
    self.assertEqual(router.route(2.0), ('MyInt', MyInt, 2))

  def test_own_constructor_trusted(self) -> None:
    """A subclass with a constructor of its own takes, through the cast
    pass, what its constructor accepts, past the rule of its builtin."""

    class Upper(str):
      def __new__(cls, value: Any) -> Any:
        return str.__new__(cls, str(value).upper())

    class Router(BaseObject):
      @overload(Upper)
      def route(self, value: Any) -> Any:
        return 'Upper', type(value), value

    self.assertEqual(Router().route(5), ('Upper', Upper, '5'))
