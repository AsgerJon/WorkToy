"""
Helpers for 'TestThisNotifiers' using the subscripted decorator form,
'@THIS[Parent].x.onGet', which is syntax only from Python 3.9 on, where
PEP 614 let a decorator be any expression. The 'test_this_notifiers.py'
module imports this module behind a 'sys.version_info' guard, so on
Python 3.7 and 3.8 this file is never parsed; the call form,
'f = THIS[Parent].x.onGet(f)', is the one those versions write, and the
test module holds it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS


# noinspection PyCompatibility
def makeBound(parent: type) -> type:
  """
  The 'makeBound' function returns a subclass of 'parent' that expands on
  the inherited 'x' through 'THIS[parent]'.
  """

  class Bound(parent):
    """Bound names its base in the reference."""

    # noinspection PyCompatibility
    @THIS[parent].x.onGet
    def _onGetBound(self, value: int) -> None:
      self.boundSaw = value

  return Bound


def makeWrong(own: type, parent: type) -> type:
  """
  The 'makeWrong' function builds a subclass of 'own' whose reference
  names 'parent', which is not a base of 'own'. The hook that places
  the clone is installed on 'parent' and runs as a subclass of 'parent'
  is created, so nothing refuses the class statement and the decoration
  is never placed; the clone stays recorded on 'parent'. The reference
  names 'x', which 'parent' holds, so the decorator itself has nothing to
  refuse. No test uses this helper until a refusal exists.
  """

  class Wrong(own):
    """Wrong names a base it does not have."""

    # noinspection PyCompatibility
    @THIS[parent].x.onGet
    def _onGetX(self, value: int) -> None:
      pass

  return Wrong
