"""
Helpers for 'TestThisSharedRecord' using the subscripted decorator form,
'@THIS[Parent].x.onSet', which is syntax only from Python 3.9 on, where
PEP 614 let a decorator be any expression. The 'test_this_shared_record.py'
module imports this module behind a 'sys.version_info' guard, so on
Python 3.7 and 3.8 this file is never parsed.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS


# noinspection PyCompatibility
def bothParents(grandParent: type, parent: type, seen: list) -> type:
  """
  The 'bothParents' function returns a subclass of 'parent' decorating the
  inherited 'x' through 'THIS[parent]' and through 'THIS[grandParent]',
  and 'y', which 'parent' holds, through 'THIS[parent]'.
  """

  class Child(parent):
    """Child names both parents."""

    @THIS[parent].x.onSet
    def _first(self, value: int) -> None:
      seen.append('first')

    @THIS[grandParent].x.onSet
    def _second(self, value: int) -> None:
      seen.append('second')

    @THIS[parent].y.onSet
    def _onY(self, value: int) -> None:
      seen.append('y')

  return Child
