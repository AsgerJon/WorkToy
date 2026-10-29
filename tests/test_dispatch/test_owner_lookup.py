"""
TestOwnerLookup subclasses 'DispatcherTest' and pins that the dispatch
machinery reads what it needs with 'type.__getattribute__' and
'object.__getattribute__', so a class hook cannot answer in its place: a
'Dispatcher' installed with 'setattr' finds its owner along the real
resolution order of the class, and 'isFlex' reports only the marker
'flexCall' sets. Both used 'getattr', so a metaclass misreporting
'__mro__' left the dispatcher unnamed, and an object answering every name
in '__getattr__' passed for wrapped.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import Dispatcher, flexCall, isFlex

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class FakeMro(type):
  """FakeMro claims a resolution order of 'object' alone."""

  def __getattribute__(cls, name: str) -> Any:
    if name == '__mro__':
      return (object,)
    return type.__getattribute__(cls, name)


class Lenient:
  """Lenient answers every name it lacks."""

  def __getattr__(self, name: str) -> Any:
    return True

  def __call__(self, *args) -> None:
    pass


def _twice(self, x: int) -> int:
  return 2 * x


class TestOwnerLookup(DispatcherTest):
  """
  TestOwnerLookup provides tests for lookups a class hook could answer.
  """

  def test_adopt_owner_real_mro(self) -> None:
    """A dispatcher set on a class whose metaclass misreports '__mro__'
    still adopts the class and the name it is held under."""

    class Plain(metaclass=FakeMro):
      pass

    dispatcher = Dispatcher()
    dispatcher.overload(int)(_twice)
    setattr(Plain, 'twice', dispatcher)
    self.assertEqual(Plain().twice(4), 8)
    self.assertIs(dispatcher.getFieldOwner(), Plain)
    self.assertEqual(dispatcher.getFieldName(), 'twice')

  def test_is_flex_lenient_object(self) -> None:
    """An object answering every name does not pass for wrapped by
    'flexCall', and a wrapped function still does."""
    self.assertFalse(isFlex(Lenient()))
    self.assertTrue(isFlex(flexCall(_twice)))
