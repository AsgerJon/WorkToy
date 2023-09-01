"""WorkToy - SYM - SymSpace
Special namespace class used by the SYM module."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.core import Bases
from worktoy.metaclass import AbstractNameSpace


class SymSpace(AbstractNameSpace):
  """WorkToy - SYM - SymSpace
  Special namespace class used by the SYM module."""

  def __init__(self, name: str, bases: Bases, **kwargs) -> None:
    AbstractNameSpace.__init__(self, name, bases, **kwargs)
    self._name = name
    self._bases = bases
    self._symbolicBaseclass = None
    self._symBase = None
    self._nameSpace = None
    self._instanceSpace = None
    
  def _setSymbolicBaseclass(self, ) -> None:
    if self._symbolicBaseclass is not None:
      from worktoy.waitaminute import ValueExistsError
      raise ValueExistsError('_symbolicBaseclass', self._symbolicBaseclass)
    for base in self._bases:
      if getattr(base, '__symbolic_baseclass__', False):
        self._symbolicBaseClass = base
        return

  def _getSym(self) -> type:
    """Getter-function for the symbolic baseclass."""
    if self._symbolicBaseclass is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_symbolicBaseclass')
    return self._symbolicBaseclass

  def _validateInstance(self, _: str, val: Any) -> bool:
    """This method is responsible for deciding if an entry in the
    namespace indicates a symbolic instance. A subclass may reimplement
    this method to customize instance selection. The default behaviour is
    to look for the '__symbolic_instance__' flag on the instance. It does
    not use the key."""
    return True if getattr(val, '__symbolic_instance__', False) else False

  def _parseData(self, ) -> None:
    """Parses the data removing the instance creations in the class body."""
    self._instanceSpace = {}
    self._nameSpace = {}
    for (key, val) in dict.items(self):
      if self._validateInstance(key, val):
        self._instanceSpace |= {key: val}
      self._nameSpace |= {key: val}

  def parseInstance(self, *args, **kwargs) -> Any:
    """Parses the arguments to a particular instance. """
    raise NotImplementedError

  def getNameSpace(self, **kwargs) -> dict:
    """Creates a special dictionary with instance creations found in the
    class body removed. During the __new__ method, metaclasses should
    transmit this special dictionary on to the super call. """
    if self._nameSpace is None:
      if kwargs.get('_recursion', False):
        creator = self._parseData
        varType = dict
        varName = '_nameSpace'
        from worktoy.waitaminute import RecursiveCreateGetError
        raise RecursiveCreateGetError(creator, varType, varName)
      self._parseData()
      return self.getNameSpace(_recursion=True)
    return self._nameSpace

  def getInstanceSpace(self, **kwargs) -> dict:
    """Getter-function for the dictionary of the named symbolic instances."""
    if self._instanceSpace is None:
      if kwargs.get('_recursion', False):
        creator = self._instanceSpace
        varType = dict
        varName = '_instances'
        from worktoy.waitaminute import RecursiveCreateGetError
        raise RecursiveCreateGetError(creator, varType, varName)
      self._parseData()
      return self.getInstanceSpace(_recursion=True)
    return self._instanceSpace
