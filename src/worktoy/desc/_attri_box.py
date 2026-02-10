"""
AttriBox implements a lazily instantiated and strongly typed descriptor
class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..core.sentinels import DELETED
from ..utilities import typeCast
from ..waitaminute import TypeException
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class AttriBox(Object):
  """
  AttriBox implements a lazily instantiated and strongly typed descriptor
  class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__ = None  # The type of the objects stored in the box.

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldType(self) -> type:
    return self.__field_type__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createFieldObject(self, ) -> Any:
    """
    Creates a new instance of the field type. When no field object exists
    for a given instance, this method is invoked to create one. This
    method creates it by passing stored positional and keyword arguments
    to the field type constructor.

    If the field type has a __set_name__ method, it is called with the
    owner and field name passed to the __set_name__ method of the
    AttriBox. Otherwise, it attempts to set the following dynamic
    attributes:
    __field_name__ - This is the name by which this instance of AttriBox
    appeared in the class body of the owning class.
    __field_owner__ - This is the class in whose body this instance of
    AttriBox appeared.
    __field_box__ - This is the instance of AttriBox itself.
    """
    instance = self.getContextInstance()
    fieldType = self.getFieldType()
    owner = type(instance)
    args = self.getPosArgs(THIS=instance, OWNER=owner, DESC=self)
    kwargs = self.getKeyArgs(THIS=instance, OWNER=owner, DESC=self)
    fieldObject = fieldType(*args, **kwargs)
    if hasattr(fieldType, '__set_name__'):
      fieldObject.__set_name__(owner, self.getFieldName())
    else:
      try:
        setattr(fieldObject, '__field_name__', self.getFieldName())
        setattr(fieldObject, '__field_owner__', owner)
        setattr(fieldObject, '__field_box__', self)
      except AttributeError:
        pass
    return fieldObject

  def __instance_get__(self, *args, **kwargs) -> Any:
    """
    Returns the value of the field for the given instance. If the value is
    not set, it initializes it with a new instance of the field type.
    """
    pvtName = self.getPrivateName()
    try:
      value = getattr(self.instance, pvtName)
    except AttributeError:
      pass
    else:
      return value
    if kwargs.get('_recursion', False):
      raise RecursionError
    fieldObject = self._createFieldObject()
    setattr(self.instance, pvtName, fieldObject)
    return self.__instance_get__(_recursion=True)

  def __instance_set__(self, value: Any, *args, **kwargs) -> None:
    """
    Sets the value of the field for the given instance. If the value is
    not set, it initializes it with a new instance of the field type.
    """
    fieldType = self.getFieldType()
    pvtName = self.getPrivateName()
    if isinstance(value, fieldType) or kwargs.get('_root', False):
      return setattr(self.instance, pvtName, value)
    #  Catch recursion
    if kwargs.get('_recursion', False):
      raise RecursionError
    #  Attempt to 'typeCast'
    try:
      castedValue = typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      raise TypeException('value', value, fieldType) from typeCastException
    else:
      return self.__instance_set__(castedValue, _recursion=True)

  def __instance_delete__(self, *args, **kwargs) -> None:
    """
    Deletes the value of the field for the given instance. If the value is
    not set, it does nothing.
    """
    pvtName = self.getPrivateName()
    setattr(self.instance, pvtName, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_getitem__(cls, fieldType: type) -> Self:
    """
    Allows the AttriBox to be used as a generic type with a specified
    field type.
    """
    self = object.__new__(cls)
    self.__field_type__ = fieldType
    return self  # noqa

  def __call__(self, *args: Any, **kwargs: Any) -> Any:
    """
    Allows the AttriBox to be called like a function, returning a new
    instance of the field type.
    """
    Object.__init__(self, *args, **kwargs)
    return self

  def __delete__(self, instance: Any, **kwargs) -> None:
    try:
      Object.__delete__(self, instance, **kwargs)
    except AttributeError as attributeError:
      fieldName = self.getFieldName()
      raise AttributeError(fieldName) from attributeError
