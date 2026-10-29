"""
TestCastAs subclasses 'DispatcherTest' and pins what the cast passes of a
'Dispatcher' do with a class outside the builtin families. A signature
over such a class is reached through a cast only when the class declares
'__cast_as__' and that hook accepts the value; a class without the hook,
a subclass of a builtin included, is reached by its instances alone and
every other call goes on to the fallback. A '__cast_as__' that is not a
classmethod raises 'UnboundCastHook' out of the call rather than being
read as a signature that merely failed to match.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import UnboundCastHook

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class MyInt(int):
  """MyInt declares no hook."""


class Count(int):
  """Count declares the hook and leans on the number family."""

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    return cls(typeCast(int, value))


class Unbound:
  """Unbound defines the hook as a plain function."""

  def __cast_as__(self, value: Any) -> Any:
    return self  # pragma: no cover


class Router(BaseObject):
  """Router overloads 'route' for the three classes and falls back."""

  @overload(MyInt)
  def route(self, value: Any) -> Any:
    return 'MyInt', type(value), value

  @overload(Count)
  def route(self, value: Any) -> Any:
    return 'Count', type(value), value

  @overload.fallback
  def route(self, *args: Any) -> Any:
    return 'fallback', args


class Broken(BaseObject):
  """Broken overloads on a class whose hook is unbound."""

  @overload(Unbound)
  def route(self, value: Any) -> Any:
    return 'unbound'  # pragma: no cover

  @overload.fallback
  def route(self, *args: Any) -> Any:
    return 'fallback'  # pragma: no cover


class TestCastAs(DispatcherTest):
  """
  TestCastAs provides tests for the cast passes of a 'Dispatcher' and
  classes declaring, or lacking, '__cast_as__'.
  """

  def test_hook_reached_through_cast(self) -> None:
    """A value the hook accepts reaches the signature as an instance of
    the class; 'MyInt' without the hook never takes a foreign value, so
    '2.0' arrives as a 'Count'."""
    router = Router()
    self.assertEqual(router.route(2.0), ('Count', Count, 2))

  def test_no_hook_goes_to_fallback(self) -> None:
    """A value no hook accepts, and that is no instance, reaches the
    fallback, while instances reach their signatures directly."""
    router = Router()
    self.assertEqual(router.route(2.5), ('fallback', (2.5,)))
    self.assertEqual(router.route('x'), ('fallback', ('x',)))
    self.assertEqual(router.route(MyInt(3)), ('MyInt', MyInt, 3))
    self.assertEqual(router.route(Count(4)), ('Count', Count, 4))

  def test_unbound_hook_raises_out_of_the_call(self) -> None:
    """An unbound hook is not a failed match: the exception escapes the
    cast passes instead of sending the call to the fallback."""
    with self.assertRaises(UnboundCastHook):
      Broken().route('x')
