"""AttriBox provides a descriptor with lazy instantiation of the
underlying object. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import DELETED
from worktoy.text import typeMsg, monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.waitaminute import VariableNotNone, MissingVariable
from worktoy.attr import AbstractBox

if TYPE_CHECKING:
  from typing import Self, Any, Callable


class AttriBox(AbstractBox):
  """AttriBox provides a descriptor with lazy instantiation of the
  underlying object. """

  def __class_getitem__(cls, fieldType: type) -> Self:
    """Get the field type."""
    self = cls()
    self._setFieldType(fieldType)
    return self

  def __call__(self, *args, **kwargs) -> Self:
    """Call the descriptor with the given arguments."""
    self._setPosArgs(*args)
    self._setKeyArgs(**kwargs)
    return self

  def _createObject(self, instance: object, ) -> Any:
    """Create the object."""
    fieldType = self._getFieldType()
    posArgs = self._getPosArgs()
    keyArgs = self._getKeyArgs()
    return fieldType(*posArgs, **keyArgs)

  def _getExistingObject(self, instance: object) -> Any:
    """Get the existing object."""
    pvtName = self.getPrivateName()
    existingObject = getattr(instance, pvtName, None)
    if existingObject is DELETED:
      e = """Attempted to access attribute '%s' from object of type: '%s',
      which has been deleted!""" % (pvtName, type(instance),)
      raise AttributeError(monoSpace(e))
    if existingObject is None:
      fieldType = self._getFieldType()
      raise MissingVariable(pvtName, fieldType)
    return existingObject

  def _setObject(self, instance: object, value: Any, **kwargs) -> None:
    """Set the object."""
    pvtName = self.getPrivateName()
    fieldType = self._getFieldType()
    if isinstance(value, fieldType):
      setattr(instance, pvtName, value)
      return
    if kwargs.get('_recursion', False):
      raise RecursionError
    try:
      newObject = fieldType(value)
    except Exception as exception:
      raise TypeError(typeMsg('value', value, fieldType, )) from exception

  def _instanceGet(self, instance: Any, **kwargs) -> Any:
    """Get the instance."""
    pvtName = self.getPrivateName()
    existingObject = getattr(instance, pvtName, None)
    if existingObject is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      newObject = self._createObject(instance, )
      setattr(instance, pvtName, newObject)
      return self._instanceGet(instance, _recursion=True)
    fieldType = self._getFieldType()
    if isinstance(existingObject, fieldType):
      return existingObject
    if existingObject is DELETED:
      e = """Attempted to access attribute '%s' from object of type: '%s',
      which has been deleted!""" % (pvtName, type(instance),)
      raise AttributeError(monoSpace(e))
    raise TypeError(typeMsg('existingObject', existingObject, fieldType, ))

  def _instanceSet(self, instance: Any, value: Any, **kwargs) -> None:
    """Set the instance."""
    pvtName = self.getPrivateName()
    if value is None:
      raise VariableNotNone(pvtName, )
    fieldType = self._getFieldType()
    if isinstance(value, fieldType):
      setattr(instance, pvtName, value)
      return
    if kwargs.get('_recursion', False):
      raise RecursionError
    return self._instanceSet(instance, fieldType(value), _recursion=True)

  def _instanceDelete(self, instance: object, **kwargs) -> None:
    """Delete the instance."""
    pvtName = self.getPrivateName()
    if getattr(instance, pvtName, None) is None:
      e = """Attempted to delete attribute '%s' from object of type: '%s', 
      which owns no such attribute!""" % (pvtName, type(instance),)
      raise AttributeError(monoSpace(e))
    setattr(instance, pvtName, DELETED)
