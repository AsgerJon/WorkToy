"""
_Attribute provides a simple implementation of the descriptor protocol.
The primary provider of descriptors in the 'worktoy' library is the
'worktoy.attr' module which depends on this module. For this reason,
this module makes use of '_Attribute' for descriptors.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..waitaminute import VariableNotNone

from . import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any


class _Attribute(AbstractObject):
  """
  _Attribute instances allow a simple write-once, read-many implementation
  of the descriptor protocol. It supports a default value, which should be
  passed to the constructor. If '__get__' is called before a value has
  been set explicitly, a default value is required and will be returned.
  This writes the value permanently to the default value, meaning that the
  instance cannot later change the value of the attribute.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __default_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs, ) -> Any:
    """
    Uses the private name created by the 'AbstractObject' parent class.
    """
    pvtName = self.getPrivateName()
    try:
      value = getattr(self.instance, pvtName)
    except AttributeError as attributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      if self.__default_value__ is None:
        raise attributeError
      self.__instance_set__(self.__default_value__, )
      return self.__instance_get__(_recursion=True, )
    else:
      if value is None:
        infoSpec = """'%s' object has no attribute '%s'"""
        typeName = self.owner.__name__
        attrName = self.getFieldName()
        info = infoSpec % (typeName, attrName)
        raise AttributeError(info)
      return value

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Sets the value of the attribute. Please note the write-once requirement.
    """
    pvtName = self.getPrivateName()
    oldValue = getattr(self.instance, pvtName, None)
    if oldValue is not None:
      raise VariableNotNone(pvtName, oldValue)
    setattr(self.instance, pvtName, value)
