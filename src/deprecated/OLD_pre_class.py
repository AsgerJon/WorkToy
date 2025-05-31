"""
PreClass provides a stateful class containing the name and hash of a class
about to be created.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..parse import maybe
from ..waitaminute import MissingVariable, VariableNotNone, TypeException

from . import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class PreClass(AbstractObject):
  """PreClass provides a stateful class containing the name and hash of a
  class about to be created."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __private_fallback__ = '__pre_class__'

  #  Private variables
  __private_name__ = None
  __class_name__ = None
  __hash_value__ = None

  #  Public variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    AbstractObject.__init__(self, *args, **kwargs)
    _hash, _name, _meta = None, None, None
    for arg in args:
      if isinstance(arg, str):
        if _name is None:
          _name = arg
          continue
        raise VariableNotNone('_name')
      if isinstance(arg, int):
        if _hash is None:
          _hash = arg
          continue
        raise VariableNotNone('_hash')
      if isinstance(arg, type):
        if _meta is None:
          _meta = arg
          continue
        raise VariableNotNone('_meta')
      if all([i is not None for i in (_name, _hash, _meta)]):
        break
    else:
      if _name is None:
        raise MissingVariable('_name', str)
      if _hash is None:
        raise MissingVariable('_hash', int)
      if _meta is None:
        raise MissingVariable('_meta', type)
    self.__hash_value__ = _hash
    self.__class_name__ = _name
    self.__meta_class__ = _meta

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __hash__(self, ) -> int:
    """
    Returns the explicitly set hash value of the PreClass object.
    """
    if self.__hash_value__ is None:
      raise MissingVariable('__hash_value__', int)
    if isinstance(self.__hash_value__, int):
      return self.__hash_value__
    name, value = '__hash_value__', self.__hash_value__
    raise TypeException(name, value, int, )

  def __getattribute__(self, key: str, ) -> Any:
    """
    This reimplementation of __getattribute__ was done by a highly skilled
    professional, do not try this at home!
    """
    if key == '__name__':
      return object.__getattribute__(self, '__class_name__')
    if key == '__class__':
      return object.__getattribute__(self, '__meta_class__')
    return AbstractObject.__getattribute__(self, key)
