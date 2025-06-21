"""
KeeHook provides the namespace hook for the KeeSpace namespace class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..static import AbstractObject
from ..mcls.hooks import AbstractHook

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

  from . import _AutoMember


class KeeHook(AbstractHook):
  """
  KeeHook provides the namespace hook for the KeeSpace namespace class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addMember(self, name: str, value: Any, **kwargs) -> None:
    """
    Add a member to the KeeSpace namespace.
    """
    if value is None:
      if kwargs.get('_recursion2', False):
        raise RecursionError
      return self._addMember(name, name, _recursion2=True)
    valueType = self._getValueType()
    if valueType is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._setValueType(type(value))
      return self._addMember(name, value, _recursion=True)
    else:
      if not isinstance(value, valueType):
        es = """Found inconsistent value type for members of the '%s' class 
        under construction. Member named: '%s' has value type: '%s', 
        while the previous values had value type: '%s'. Values passed to 
        'auto' must be of the same type for the same enumeration!"""
        clsName = self.space.getClassName()
        actName = type(value).__name__
        expName = valueType.__name__
        e = es % (clsName, name, actName, expName)
        raise NotImplementedError(e)
    existing = self.space.get('__future_entries__', {})
    if name in existing:
      raise NotImplementedError('duplicate keenum: %s' % name)
    existing[name] = value
    self.space['__future_entries__'] = existing

  def _setValueType(self, valueType: type, ) -> None:
    """
    Set the value type for the KeeSpace namespace.
    """
    if '__future_value_type__' in self.space:
      existingType = self.space['__future_value_type__']
      if valueType is not existingType:
        es = """Found inconsistent value type for members of the '%s' class 
        under construction. The value type was previously set to: '%s', 
        while the new value type is: '%s'. Values passed to 'auto' must be 
        of the same type for the same enumeration!"""
        clsName = self.space.getClassName()
        e = es % (clsName, existingType.__name__, valueType.__name__)
        raise NotImplementedError(e)
      return
    self.space['__future_value_type__'] = valueType

  def _getValueType(self) -> type:
    """
    Get the value type for the KeeSpace namespace.
    """
    return self.space.get('__future_value_type__', None)

  def setItemHook(self, key: str, value: Any, oldValue: Any, ) -> bool:
    """
    The setItemHook method is called when an item is set in the
    namespace.
    """
    if isinstance(value, AbstractObject):
      if hasattr(value, '__auto_member__'):
        if getattr(value, '__auto_member__'):
          if TYPE_CHECKING:  # pragma: no cover
            assert isinstance(value, _AutoMember)
          self._addMember(key.upper(), value.getValue())
          return True
    return False

  def preCompileHook(self, compiledSpace: dict) -> dict:
    """Hook for preCompile. This is called before the __init__ method of
    the namespace object is called. The default implementation does nothing
    and returns the contents unchanged. """
    futureEntries = compiledSpace.get('__future_entries__', None)
    if futureEntries is None:
      compiledSpace['__future_entries__'] = dict()
    return compiledSpace
