"""
_Priority exposes the priority of the accessor hook through the descriptor
protocol.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...parse import maybe
from ...static import AbstractObject
from ...waitaminute import TypeException, VariableNotNone

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, TypeAlias
  from . import AbstractDescriptorHook as Hook
 
  Hooks: TypeAlias = tuple[Hook, ...]


class _Priority(AbstractObject):
  """
  _Priority exposes the priority of the accessor hook through the descriptor
  protocol.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_name__ = '__priority_value__'
  __fallback_value__ = 255

  #  Private Variables
  __private_name__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getPrivateName(self) -> str:
    """
    Reimplements the private name.
    """
    return maybe(self.__private_name__, self.__fallback_name__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs, ) -> Any:
    """
    Looks for '__priority_value__' in the instance and returns it.
    """
    pvtName = self.getPrivateName()
    try:
      out = getattr(self.instance, pvtName)
    except AttributeError:
      return self.__fallback_value__
    else:
      return maybe(out, self.__fallback_value__)
    finally:
      pass

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Sets the '__priority_value__' in the instance.
    """
    pvtName = self.getPrivateName()
    if value is None:
      raise VariableNotNone(pvtName, value)
    if not isinstance(value, int):
      raise TypeException(pvtName, value, int)
    if (255 - value) * (0 - value) < 0:
      raise NotImplementedError('TODO: IntervalError')
    setattr(self.instance, pvtName, value)
