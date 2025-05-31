"""AbstractField provides an implementation of the descriptor protocol
that allow the owning class to explicitly define the accessor methods.  """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from types import MethodType as Meth

from ..static.zeroton import DELETED
from ..waitaminute import attributeErrorFactory, TypeException, \
  ProtectedError, ReadOnlyError

from . import _FieldProperties, _flexSet, _flexDelete

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class Field(_FieldProperties):
  """AbstractField provides an implementation of the descriptor protocol
  that allow the owning class to explicitly define the accessor methods.  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  #  # Accessor decorators
  GET = _FieldProperties._setGetter
  SET = _FieldProperties._addSetter
  DELETE = _FieldProperties._addDeleter
  #  # Notifier decorators
  preGET = _FieldProperties._addPreGet
  preSET = _FieldProperties._addPreSet
  preDELETE = _FieldProperties._addPreDelete
  postGET = _FieldProperties._addPostGet
  postSET = _FieldProperties._addPostSet
  postDELETE = _FieldProperties._addPostDelete

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Reimplementation inserting the hooks.
    """
    self.__current_instance__ = instance
    self.__current_owner__ = owner
    if instance is None:
      return self
    value = self.__instance_get__()
    if value is DELETED:
      _name = self.__field_name__
      raise attributeErrorFactory(self.owner, _name)
    self._notifyPreGet(value)
    try:
      return value
    finally:
      self._notifyPostGet(value)

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    Reimplementation inserting the hooks.
    """
    self.__current_instance__ = instance
    self.__current_owner__ = type(instance)
    try:
      oldVal = self.__instance_get__()
    except Exception as exception:
      oldVal = exception
    else:
      pass
    postSet = self._notifyPostSet
    self._notifyPreSet(value, oldVal)
    self.__instance_set__(value, oldVal=oldVal, )
    self._notifyPostDelete(oldVal)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    Reimplementation inserting the hooks.
    """
    self.__current_instance__ = instance
    self.__current_owner__ = type(instance)
    try:
      oldVal = self.__instance_get__(**kwargs)
    except Exception as exception:
      type_, name = self.owner, self.__field_name__
      raise attributeErrorFactory(type_, name) from exception
    else:
      pass

    self._notifyPreDelete(oldVal)
    self.__instance_delete__(oldVal=oldVal, )
    self._notifyPostDelete(oldVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _notifyPreGet(self, value: Any) -> None:
    """
    Notifies the pre-get listeners.
    """
    preGets = self._getPreGet()
    for preGet in preGets:
      preGet(self.instance, value, )

  def _notifyPostGet(self, value: Any) -> None:
    """
    Notifies the post-get listeners.
    """
    postGets = self._getPostGet()
    for postGet in postGets:
      postGet(self.instance, value, )

  def _notifyPreSet(self, value: Any, oldValue: Any) -> None:
    """
    Notifies the pre-set listeners.
    """
    preSets = self._getPreSet()
    for preSet in preSets:
      preSet(self.instance, value, oldValue, )

  def _notifyPostSet(self, value: Any, oldValue: Any) -> None:
    """
    Notifies the post-set listeners.
    """
    postSets = self._getPostSet()
    for postSet in postSets:
      postSet(self.instance, value, oldValue, )

  def _notifyPreDelete(self, oldValue: Any) -> None:
    """
    Notifies the pre-delete listeners.
    """
    preDeletes = self._getPreDelete()
    for preDelete in preDeletes:
      preDelete(self.instance, oldValue, )

  def _notifyPostDelete(self, oldValue: Any) -> None:
    """
    Notifies the post-delete listeners.
    """
    postDeletes = self._getPostDelete()
    for postDelete in postDeletes:
      postDelete(self.instance, oldValue, )

  def __instance_get__(self, **kwargs) -> Any:
    """
    Returns the value of the field.
    """
    getter = self._getGet()
    return getter(self.instance)

  def __instance_set__(self, val: Any, oldVal: Any = None, **kwargs) -> None:
    """
    Sets the value of the field.
    """
    setters = self._getSet()
    if not setters:
      raise ReadOnlyError(self.instance, self, val)
    for setter in setters:
      try:
        setter(self.instance, val, old=oldVal, )
      except TypeError as typeError:
        if 'unexpected keyword argument' in str(typeError):
          try:
            setter(self.instance, val)
          except Exception as exception:
            raise exception from typeError

  def __instance_delete__(self, oldVal: Any = None, **kwargs) -> None:
    """
    Deletes the value of the field.
    """
    deleters = self._getDelete()
    if not deleters:
      raise ProtectedError(self, self.instance, oldVal)
    for deleter in deleters:
      deleter(self.instance, old=oldVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
