"""
TestOverloadAfterDel subclasses 'OverloadTest' and pins that a name the
class body binds plainly and then deletes may be overloaded afterwards.
'LoadSpaceHook' records every plain binding so that a name is not both
overloaded and defined plainly in one body, and it used to keep that
record past the deletion, so 'f = 1', 'del f', '@overload(int) def f'
raised 'OverloadConflict' although no plain binding survived. The hook
now forgets the name in the deletion phase. A deleted overload stays
refused with 'ClaimedName', as before.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import ClaimedName, OverloadConflict

from . import OverloadTest


class TestOverloadAfterDel(OverloadTest):
  """
  TestOverloadAfterDel provides tests for overloading a name the body
  bound plainly and deleted.
  """

  def test_plain_then_del_then_overload(self) -> None:
    """The deleted plain binding no longer blocks the overload."""

    class Host(BaseObject):
      f = 1
      del f

      @overload(int)
      def f(self, x: int) -> str:
        return 'int %d' % x

    self.assertEqual(Host().f(3), 'int 3')

  def test_plain_without_del_still_conflicts(self) -> None:
    """A plain binding still present still conflicts."""
    with self.assertRaises(OverloadConflict):
      class Host(BaseObject):
        f = 1

        @overload(int)
        def f(self, x: int) -> str:
          return 'int'  # pragma: no cover

  def test_deleted_overload_still_claimed(self) -> None:
    """Deleting an overloaded name is still refused as the class is
    created."""
    with self.assertRaises(ClaimedName):
      class Host(BaseObject):
        @overload(int)
        def f(self, x: int) -> str:
          return 'int'  # pragma: no cover

        del f
