"""
FixBox subclasses 'AttriBox' and provides a descriptor for immutable
attributes. The only change reimplemented is that setting is only allowed
when no value has been set before.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.desc import AttriBox
from worktoy.waitaminute.desc import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class FixBox(AttriBox):
  """
  FixBox subclasses 'AttriBox' and provides a descriptor for immutable
  attributes. The only change reimplemented is that setting is only allowed
  when no value has been set before.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """Set the value once; subsequent assignments raise
    'WriteOnceError'. Uses 'AttributeError' (not 'is None') to
    detect the unset state, so that an explicit assignment of
    'None' still counts as a write."""
    pvtName = self.getPrivateName()
    try:
      oldValue = object.__getattribute__(instance, pvtName)
    except AttributeError:
      pass
    else:
      raise WriteOnceError(self, oldValue, value)
    AttriBox.__instance_set__(self, instance, value, **kwargs)

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """Deletion is disabled on 'FixBox'. Falls through to
    'Object.__instance_delete__', which raises 'ProtectedError'."""
    Object.__instance_delete__(self, instance, *_, **kwargs)
