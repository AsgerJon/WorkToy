"""
TestNotification tests when the notification callbacks of a
'BaseDescriptor' fire, measured by what each one sees of the value. A
'pre' callback fires before the access takes effect and an 'on' callback
after it: 'preSet' still reads the old value and 'onSet' the new one,
'preDelete' can still read the value while 'onDelete' finds it gone, and
'onGet' receives the value the read returns.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestNotification(DescTest):
  """
  TestNotification tests what each notification callback of a
  'BaseDescriptor' sees of the value it is notified about.
  """

  @staticmethod
  def _buildOwner(seen: list) -> type:
    """The '_buildOwner' method builds a class with two 'AttriBox' fields:
    'watched' carries the set and delete callbacks and 'read' the get
    callbacks, so reading 'watched' inside a callback fires no further
    callbacks. Each callback records what it sees in 'seen'."""

    class Owner(BaseObject):
      watched = AttriBox[int](0)
      read = AttriBox[int](7)

      @watched.preSet
      def _preSetWatched(self, value: Any) -> None:
        seen.append(('preSet', value, self.watched))

      @watched.onSet
      def _onSetWatched(self, value: Any) -> None:
        seen.append(('onSet', value, self.watched))

      @watched.preDelete
      def _preDeleteWatched(self) -> None:
        seen.append(('preDelete', self.watched))

      @watched.onDelete
      def _onDeleteWatched(self) -> None:
        seen.append(('onDelete', hasattr(self, 'watched')))

      @read.preGet
      def _preGetRead(self) -> None:
        seen.append(('preGet',))

      @read.onGet
      def _onGetRead(self, value: Any) -> None:
        seen.append(('onGet', value))

    return Owner

  def test_set_notifications(self) -> None:
    """'preSet' sees the incoming value while the old one is stored, and
    'onSet' sees it once it is stored."""
    seen = []
    owner = self._buildOwner(seen)()
    owner.watched = 5
    self.assertEqual(seen, [('preSet', 5, 0), ('onSet', 5, 5)])

  def test_get_notifications(self) -> None:
    """'preGet' fires before the read, and 'onGet' receives the value the
    read then returns."""
    seen = []
    owner = self._buildOwner(seen)()
    self.assertEqual(owner.read, 7)
    self.assertEqual(seen, [('preGet',), ('onGet', 7)])

  def test_delete_notifications(self) -> None:
    """'preDelete' can still read the value, and 'onDelete' finds it
    gone."""
    seen = []
    owner = self._buildOwner(seen)()
    owner.watched = 5
    del seen[:]
    del owner.watched
    self.assertEqual(seen, [('preDelete', 5), ('onDelete', False)])
