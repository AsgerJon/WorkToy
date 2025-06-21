"""
ZeroSpace provides the namespace objects for the Zeroton metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...waitaminute import ReservedName
from .. import HistDict
from . import _reservedNames

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Any

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class ZeroSpace(HistDict):
  """
  ZeroSpace provides the namespace objects for the Zeroton metaclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _isRoot(obj: object) -> bool:
    """
    Check if the object is a root object.
    """
    trust = getattr(obj, '__trust_me_bro__', None)
    return False if trust is None else (True if trust else False)

  def __init__(self, mcls: type, name: str, bases: Bases, **kwargs) -> None:
    """
    Initialize the ZeroSpace with the given arguments.
    """
    self.__meta_class__ = mcls
    self.__class_name__ = name
    self.__base_classes__ = bases
    self.__key_args__ = kwargs.get('keyArgs', None)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setitem__(self, key: str, value: object, **kwargs) -> None:
    """
    Set the item in the ZeroSpace.
    """
    if key in _reservedNames and not self._isRoot(value):
      raise ReservedName(key)
    return HistDict.__setitem__(self, key, value)

  def compile(self, ) -> Space:
    """
    Compiles the namespace to an instance of a traditional 'dict'.
    """
    out = dict()
    for call in self.getItemCalls():
      call.apply(out)
    return out
