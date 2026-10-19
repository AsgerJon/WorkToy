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

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias, Callable
  from . import KeeMeta

  __INIT__: TypeAlias = Callable[[KeeMeta, Kee], None]
  __GET__: TypeAlias = Callable[[KeeMeta, KeeMeta, Type[KeeMeta]], Any]


class KeeSpaceHook(AbstractSpaceHook):
  """
  KeeSpaceHook collects the 'Kee' descriptors encountered in the
  class bodies of KeeNum classes. This happens during the
  'setItemPhase'. To avoid context leakage, the members are collected
  in the owning namespace object. The namespace object is expected to
  implement an 'addNum' method which KeeSpaceHook calls to register
  each Kee. The hook provides no further functionality than deciding
  which key, value pairs to collect as future members of the
  enumeration.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    Routes 'Kee' objects to the 'addNum' method of the present namespace
    object. A '__class_resolve__' that is a plain function or a
    staticmethod raises 'UnboundClassHook', as a routed '__class_*__'
    hook does: the lookups call the hook bound to the class.

    A name bound both to a 'Kee' and to a plain value, in either order,
    raises 'KeeMemberNameError': the member would replace the attribute
    without a word, as the 'Kee' is routed past the namespace while the
    plain value is stored in it. Two 'Kee' objects of one name raise
    'KeeDuplicate' from 'addNum', as before.
    """
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
