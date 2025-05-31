"""
'PreClassHook' replaces 'THIS' in the AbstractNamespace with 'PreClass'
objects having the hash and name of the future class ahead of class creation.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from ...static import PreClass, HistDict, TypeSig
from ...static.zeroton import THIS
from ...waitaminute import TypeException

from . import AbstractHook

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, TypeAlias


class PreClassHook(AbstractHook):
  """
  'PreClassHook' replaces 'THIS' in the AbstractNamespace with 'PreClass'
  objects having the hash and name of the future class ahead of class
  creation.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __pre_class__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createPreClass(self, **kwargs) -> None:
    """
    Creates the unique 'PreClass' object for the namespace instance owning
    this hook instance.
    """
    _hash = self.space.getHash()
    _name = self.space.getClassName()
    _meta = self.space.getMetaclass()
    self.__pre_class__ = PreClass(_hash, _name, _meta)

  def _getPreClass(self, **kwargs) -> PreClass:
    """
    Getter-function for the 'PreClass' for the namespace instance owning
    this hook instance.
    """
    if self.__pre_class__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createPreClass()
      return self._getPreClass(_recursion=True)
    if isinstance(self.__pre_class__, PreClass):
      return self.__pre_class__
    raise TypeException('__pre_class__', self.__pre_class__, PreClass, )

  def setItemHook(self, key: str, val: Any, old: Any, ) -> bool:
    """
    If key contains reference the class under construction by containing
    'THIS', replace with 'PreClass' object providing the hash and name of the
    future class.
    """
    preClass = self._getPreClass()
    typeSigs = getattr(val, '__type_sigs__', None)
    if typeSigs is None:
      return False
    for sig in typeSigs:
      if isinstance(sig, TypeSig):
        TypeSig.replaceTHIS(sig, preClass, )
        _ = hash(sig)
        continue
      raise TypeException('sig', sig, TypeSig, )
    else:
      return False

  def postCompileHook(self, compiledSpace) -> dict:
    """
    Where a type signature in the overload map includes a base class,
    we create a new type signature pointing to the same function, but with
    the 'PreClass' object replacing the base class. This will allow 'THIS'
    defined in an overload in a parent to work in the child class with
    either an instance of the parent or the child.
    """
    overloadMap = self.space.getOverloadMap()  # str: dict[TypeSig, Func]
    preClass = self._getPreClass()
    bases = self.space.getClassBases()
    newLoadMap = dict()
    for key, sigMap in overloadMap.items():
      moreSigMap = dict()
      for sig, func in sigMap.items():
        newSig = []
        for type_ in sig:
          if type_ in bases:
            newSig.append(preClass)
            continue
          newSig.append(type_)
        else:
          if preClass in newSig:
            newTypeSig = TypeSig(*newSig)
            moreSigMap[newTypeSig] = func
          moreSigMap[sig] = func
      else:
        newLoadMap[key] = moreSigMap
    else:
      self.space.__overload_map__ = newLoadMap
    return compiledSpace
