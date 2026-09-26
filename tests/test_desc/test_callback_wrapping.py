"""
TestCallbackWrapping subclasses 'DescTest' from the 'tests.test_desc'
package and pins how the notification callbacks of a 'BaseDescriptor'
are called. The descriptor calls each callback with the instance and,
for the get and set callbacks, the value, and a callback may declare
fewer parameters than that, since the call goes through 'flexCall'. The
decorators wrap the callback once, as the class body runs, so an access
reuses that wrapper instead of building a new one each time. A subclass
that replaces a callback by name with an undecorated method still has it
called the same way.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.dispatch import isFlex
from worktoy.mcls import BaseObject

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

_CALLBACK_NAMES = (
  '_preGet',
  '_onGet',
  '_preSet',
  '_onSet',
  '_preDelete',
  '_onDelete',
)


class TestCallbackWrapping(DescTest):
  """
  TestCallbackWrapping provides tests for the notification callbacks of
  'BaseDescriptor' and the 'flexCall' wrapping they receive.
  """

  @staticmethod
  def _buildOwner(base: type, calls: list) -> type:
    """The '_buildOwner' method builds a class derived from 'base' with
    one 'AttriBox' field carrying a callback of every kind. Each callback
    declares only 'self' and records its name in 'calls'."""

    class Owner(base):
      bar = AttriBox[int](0)

      @bar.preGet
      def _preGet(self) -> None:
        calls.append('_preGet')

      @bar.onGet
      def _onGet(self) -> None:
        calls.append('_onGet')

      @bar.preSet
      def _preSet(self) -> None:
        calls.append('_preSet')

      @bar.onSet
      def _onSet(self) -> None:
        calls.append('_onSet')

      @bar.preDelete
      def _preDelete(self) -> None:
        calls.append('_preDelete')

      @bar.onDelete
      def _onDelete(self) -> None:
        calls.append('_onDelete')

    return Owner

  def test_callbacks_wrapped_on_plain_owner(self) -> None:
    """On an owner that is not a 'BaseObject', every decorated callback
    is stored wrapped by 'flexCall'."""
    owner = self._buildOwner(object, [])
    for name in _CALLBACK_NAMES:
      with self.subTest(name=name):
        self.assertTrue(isFlex(owner.__dict__[name]))

  def test_callbacks_wrapped_on_base_object(self) -> None:
    """On a 'BaseObject' owner, every decorated callback is stored
    wrapped by 'flexCall' as well."""
    owner = self._buildOwner(BaseObject, [])
    for name in _CALLBACK_NAMES:
      with self.subTest(name=name):
        self.assertTrue(isFlex(owner.__dict__[name]))

  def test_callbacks_take_fewer_parameters(self) -> None:
    """Each callback declares only 'self', yet a read, a write and a
    deletion each call theirs in order without error."""
    for base in (object, BaseObject):
      with self.subTest(base=base.__name__):
        calls = []
        owner = self._buildOwner(base, calls)()
        owner.bar = 7
        self.assertEqual(owner.bar, 7)
        del owner.bar
        expected = [
          '_preSet', '_onSet', '_preGet', '_onGet', '_preDelete', '_onDelete',
        ]
        self.assertEqual(calls, expected)

  def test_override_by_plain_method(self) -> None:
    """A subclass replacing a callback by name with an undecorated method
    that declares fewer parameters has its method called in place of the
    original, which still fires for instances of the parent."""
    calls = []

    class Parent(BaseObject):
      bar = AttriBox[int](0)

      @bar.onSet
      def _onSetBar(self, value: Any) -> None:
        calls.append(('parent', value))

    class Child(Parent):
      def _onSetBar(self) -> None:
        calls.append(('child',))

    child = Child()
    child.bar = 7
    self.assertEqual(child.bar, 7)
    parent = Parent()
    parent.bar = 8
    self.assertEqual(calls, [('child',), ('parent', 8)])
