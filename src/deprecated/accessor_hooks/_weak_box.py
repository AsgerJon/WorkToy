"""
WeakBox caches values as dynamic attributes on instances. This is in
contrast to 'CachingHook' which caches values on the descriptor side.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from ...waitaminute import MissingVariable, TypeException, VariableNotNone
from . import AbstractDescriptorHook

#  Below provides compatibility back to Python 3.7
try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any

ic.configureOutput(includeContext=True, )


class WeakBox(AbstractDescriptorHook):
  """
  WeakBox provides a descriptor hook for the lazy descriptors.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __field_type_key__ = '__box_type_%s_'

  #  Fallback Variables

  #  Private Variables

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFieldTypeKey(self) -> str:
    """
    Returns the key used to store the field type in the instance.
    """
    if self.__field_type_key__ is None:
      raise MissingVariable('WeakBox.__field_type_key__')
    if isinstance(self.__field_type_key__, str):
      return self.__field_type_key__ % self.desc.getPrivateName()
    name, value = '__field_type_key__', self.__field_type_key__
    raise TypeException(name, value, str, )

  def getFieldType(self) -> type:
    """
    Returns the field type of the BoxHook.
    """
    fieldTypeKey = self._getFieldTypeKey()
    return getattr(self.desc, fieldTypeKey, None)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setFieldType(self, fieldType: type) -> None:
    """
    Sets the field type of the BoxHook.
    """
    if not isinstance(fieldType, type):
      raise TypeException('fieldType', fieldType, type, )
    fieldTypeKey = self._getFieldTypeKey()
    setattr(self.desc, fieldTypeKey, fieldType)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preGet(self, value: Any = None) -> Any:
    """
    Looks for an existing value already existing on the instance at the
    private name of this descriptor.
    """
    privateName = self.desc.getPrivateName()
    return getattr(self.activeInstance, privateName, None)

  def postGet(self, value: Any) -> Any:
    """
    This method is called after this hook failed to provide a cached value
    during the previous 'preGet' phase. If the value received now is
    'None', it indicates that the '__instance_get__' on the owning
    descriptor could not provide a value. In this case, this hook has no
    remedy and does nothing. If the value is not 'None', the value is
    cached for future use.

    A subclass wishing to provide type-guarding or type-casting should do
    so and pass the result to a super call to this method.
    """
    if value is None:
      return
    privateName = self.desc.getPrivateName()
    setattr(self.activeInstance, privateName, value)

  def postSet(self, newValue: Any, oldValue: Any, ) -> Any:
    """
    If the 'newValue' is already cached, this method does nothing.
    Otherwise, it caches the 'newValue' on the currently active instance.

    A subclass wishing to provide type-guarding or type-casting should do
    so and pass the result to a super call to this method.
    """
    privateName = self.desc.getPrivateName()
    cachedValue = getattr(self.activeInstance, privateName, None)
    if cachedValue is newValue:
      return
    setattr(self.activeInstance, privateName, newValue)
