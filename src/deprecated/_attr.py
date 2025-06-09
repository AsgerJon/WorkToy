"""
'Attr' provides a descriptor exposing a private attribute to public access.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..static import AbstractObject
from ..waitaminute import MissingVariable, TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class Attr(AbstractObject):
  """Creates a deferred function that is called when the __get__ is first
  called. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __private_name__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getPrivateName(self, **kwargs) -> str:
    """
    Getter-function for the private name.
    """
    if self.__private_name__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      name = AbstractObject.getPrivateName(self, )
      self._setPrivateName(name, )
      return self._getPrivateName(_recursion=True, )
    if isinstance(self.__private_name__, str):
      return self.__private_name__
    name, value = '__private_name__', self.__private_name__
    raise TypeException(name, value, str)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setPrivateName(self, privateName: str) -> Self:
    """
    Setter-function for the private name.
    """
    if self.__private_name__ is not None:
      raise MissingVariable('__private_name__', str)
    if not isinstance(privateName, str):
      name, value = '_setPrivateName', privateName
      raise TypeException(name, value, str)
    self.__private_name__ = privateName
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, privateName: str = None) -> None:
    """
    Constructor for the Attr descriptor.
    """
    if privateName is not None:
      self._setPrivateName(privateName)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, **kwargs) -> Any:
    """
    Instance getter for the Attr descriptor.
    """
    pvtName = self._getPrivateName()
    try:
      out = getattr(self.instance, pvtName, )
    except Exception as exception:
      raise exception
    else:
      return out
    finally:
      pass

  def __instance_set__(self, value: Any, **kwargs) -> None:
    """
    Instance setter for the Attr descriptor.
    """
    pvtName = self._getPrivateName()
    try:
      oldValue = getattr(self.instance, pvtName, )
    except Exception as exception:
      if isinstance(exception, AttributeError):
        oldValue = None
      else:
        raise exception
    else:
      if oldValue is value:
        return
      setattr(self.instance, pvtName, value)
    finally:
      pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
