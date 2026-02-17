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
from worktoy.waitaminute import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class FixBox(AttriBox):
  """
  FixBox subclasses 'AttriBox' and provides a descriptor for immutable
  attributes. The only change reimplemented is that setting is only allowed
  when no value has been set before.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _inspectValue(self, ) -> Any:
    """
    Retrieves the value without invoking side effects.
    """
    pvtName = self.getPrivateName()
    try:
      value = object.__getattribute__(self.instance, pvtName)
    except AttributeError:
      return None
    else:
      return value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    oldValue = self._inspectValue()
    if oldValue is not None:
      raise WriteOnceError(self, oldValue, value)
    AttriBox.__instance_set__(self, instance, value, **kwargs)

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
      ) -> None:
    Object.__instance_delete__(self, instance, old, **kwargs)
