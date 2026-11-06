"""
KeeSpaceHook collects the 'Kee' descriptors from a 'KeeNum' class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..mcls.space_hooks import AbstractSpaceHook
from ..waitaminute.keenum import KeeMemberNameError
from ..waitaminute.meta import UnboundClassHook
from . import Kee

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Type, TypeAlias, Callable
  from . import KeeMeta

  __INIT__: TypeAlias = Callable[[KeeMeta, Kee], None]
  __GET__: TypeAlias = Callable[[KeeMeta, KeeMeta, Type[KeeMeta]], Any]


class KeeSpaceHook(AbstractSpaceHook):
  """
  An enumeration body binds its members as ordinary names, 'RED =
  Kee[int](1)', yet the class must hold members at those names and
  nothing else: a plain value bound at a member's name, before or after
  the member, would be replaced without a word. The 'Kee' objects must
  therefore reach the namespace's record and never its dictionary, and
  a body binding a member's name twice must fail at that line.

  Implementation
  --------------

  'setItemPhase' hands every 'Kee' to 'addNum' of the namespace and
  claims the binding. A 'Kee' bound at a name the dictionary holds, or
  a plain value bound at a name a member takes, declared or inherited,
  raises 'KeeMemberNameError'; two 'Kee' objects of one name raise
  'KeeDuplicate' from 'addNum'. A '__class_resolve__' bound to a plain
  function or a staticmethod raises 'UnboundClassHook', as a routed
  class hook does, since the lookups call the hook bound to the class.
  One hook object serves every body, so it keeps nothing of its own.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    if key == '__class_resolve__':
      if isinstance(val, (FunctionType, staticmethod)):
        raise UnboundClassHook(self.space.getClassName(), key)
    if isinstance(val, Kee):
      if dict.__contains__(self.space, key):
        raise KeeMemberNameError(self.space.getClassName(), key)
      self.space.addNum(key, val)
      return True
    if self.space.hasNum(key):
      raise KeeMemberNameError(self.space.getClassName(), key)
    return False
