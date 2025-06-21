"""
NestBox subclasses 'AttriBox' and provides a descriptor intended for use
by other descriptors.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import AttriBox, _TopInstance, _TopOwner
from ..static import Alias, AbstractObject
from ..static.zeroton import DELETED
from ..waitaminute import TypeException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Self


class NestBox(AttriBox):
  """
  NestBox subclasses 'AttriBox' and provides a descriptor intended for use
  by other descriptors. This means that the object at the 'instance'
  attribute is itself a descriptor and the actual instance is that of the
  owning instance. To facilitate this, the 'Alias' descriptor adds 'desc'
  and 'descType' as alternative names for the 'instance' and 'owner'
  respectively. Finally, the 'topInstance' and 'topOwner' attributes
  are provided to access the top-level instance and owner of the descriptor.
  Those are the objects that are not descriptors.

  - instance: The immediate owning instance of this descriptor.
  - owner: The immediate owning class of this descriptor.
  - desc: An alias for 'instance'
  - descType: An alias for 'owner'
  - topInstance: The top-level instance of the descriptor.
  - topOwner: The top-level owner of the descriptor.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  desc = Alias('instance')
  descType = Alias('owner')
  topInstance = _TopInstance()
  topOwner = _TopOwner()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createFieldObject(self, ) -> Any:
    """
    Creates the field object using the type specified in the AttriBox.
    This method is used by the 'strongBox' to instantiate the field
    object when it is not already cached.
    """
    fieldType = self.getFieldType()
    ins, own, desc = self.topInstance, self.topOwner, self.desc
    args = self._getPositionalArgs(THIS=ins, OWNER=own, DESC=desc)
    kwargs = self._getKeywordArgs(THIS=ins, OWNER=own, DESC=desc)
    return fieldType(*args, **kwargs)

  def __instance_get__(self, **kwargs, ) -> Any:
    """
    Attempts to retrieve the value of the field object from the instance.
    If the value is 'None', or if 'getattr' raises 'AttributeError',
    a new 'fieldObject' is created and set on the instance and the
    method recurses to retrieve the value again. This ensures that the
    retrieval does work.
    """
    pvtName = self.getPrivateName()
    try:
      value = getattr(self.topInstance, pvtName, )
    except AttributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError
      value = self._createFieldObject()
      setattr(self.topInstance, pvtName, value)
      return self.__instance_get__(_recursion=True)
    else:
      if value is None:
        if kwargs.get('_recursion2', False):
          raise RecursionError
        value = self._createFieldObject()
        setattr(self.topInstance, pvtName, value)
        return self.__instance_get__(_recursion2=True)
      return value

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Implements type guard.
    """
    fieldType = self.getFieldType()
    if isinstance(value, fieldType):
      pvtName = self.getPrivateName()
      return setattr(self.topInstance, pvtName, value)
    if kwargs.get('_recursion', False):
      raise RecursionError
    try:
      castValue = fieldType(value)
    except Exception as exception:
      raise TypeException('value', value, fieldType, ) from exception
    else:
      return self.__instance_set__(castValue, _recursion=True)

  def __instance_delete__(self, **kwargs) -> None:
    """
    AttriBox sets the value to the 'DELETED' sentinel value.
    """
    setattr(self.topInstance, self.getPrivateName(), DELETED)
