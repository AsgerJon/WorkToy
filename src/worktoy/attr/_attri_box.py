"""AttriBox provides a descriptor with lazy instantiation of the
underlying object. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..static import AbstractObject
from ..static.zeroton import DELETED
from ..waitaminute import MissingVariable, TypeException, VariableNotNone

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class AttriBox(AbstractObject):
  """
  AttriBox provides a descriptor with lazy instantiation of the
  underlying object.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldType(self) -> type:
    """
    Returns the type of the field object.
    """
    if self.__field_type__ is None:
      raise MissingVariable('AttriBox.__field_type__')
    if isinstance(self.__field_type__, type):
      return self.__field_type__
    name, value = '__field_type__', self.__field_type__
    raise TypeException(name, value, type)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setFieldType(self, fieldType: type) -> None:
    """
    Sets the type of the field object.
    """
    if self.__field_type__ is not None:
      raise VariableNotNone('AttriBox.__field_type__', self.__field_type__)
    if not isinstance(fieldType, type):
      raise TypeException('fieldType', fieldType, type)
    self.__field_type__ = fieldType

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, fieldType: type) -> None:
    """
    Initializes the AttriBox with the type of the object to be returned.
    """
    self.setFieldType(fieldType)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_getitem__(cls, fieldType: type) -> Self:
    """
    Returns a new AttriBox with the specified field type.
    """
    return cls(fieldType)

  def __call__(self, *args, **kwargs) -> Any:
    """
    This method pretends to be the actual constructor.
    """
    self.__pos_args__ = (*args,)
    self.__key_args__ = {**kwargs, }
    return self

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
    ins, own = self.instance, self.owner
    args = self._getPositionalArgs(THIS=ins, OWNER=own)
    kwargs = self._getKeywordArgs(THIS=ins, OWNER=own)
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
      value = getattr(self.instance, pvtName, )
    except AttributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError
      value = self._createFieldObject()
      setattr(self.instance, pvtName, value)
      return self.__instance_get__(_recursion=True)
    else:
      if value is None:
        if kwargs.get('_recursion2', False):
          raise RecursionError
        value = self._createFieldObject()
        setattr(self.instance, pvtName, value)
        return self.__instance_get__(_recursion2=True)
      return value

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Implements type guard.
    """
    fieldType = self.getFieldType()
    if isinstance(value, fieldType):
      pvtName = self.getPrivateName()
      return setattr(self.instance, pvtName, value)
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
    setattr(self.instance, self.getPrivateName(), DELETED)
