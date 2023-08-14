"""AccessorError is a custom Exception raised when an attempt is made to
access a property in a disallowed way. This is an abstract class intended
to be further subclassed to specific access operations. These should
implement the abstract method getOperation defining the disallowed
operation."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never


class AccessorError(Exception):
  """AccessorError is a custom Exception raised when an attempt is made to
  access a property in a disallowed way."""

  def __init__(self, name: str) -> None:
    self._varName = name

  @abstractmethod
  def _getOperation(self) -> str:
    """Getter-function for the illegal operation attempted"""

  def _getVarName(self, ) -> str:
    """Getter-function for the name of the variable"""
    if isinstance(self._varName, str):
      return self._varName
    raise TypeError

  def _setVarName(self, *_) -> Never:
    """LOL"""
    msg = """Yo dawg, heard you like read-only errors, so we put a read 
    only error into your read only error! Variable: %s"""
    raise TypeError(msg % self._getVarName())

  def _delVarName(self, *_) -> Never:
    """LOL"""
    msg = """Attempted to delete protected variable! Currently: %s"""
    raise TypeError(msg % self._getVarName())

  varName = property(_getVarName, _setVarName, _delVarName)

  def __repr__(self, ) -> str:
    """Code representation"""
    cls = self.__class__.__qualname__
    return '%s(%s, %s)' % (cls, self.varName, self._getOperation())

  def __str__(self) -> str:
    """String representation"""
    msg = 'Attempted operation \'%s\' on variable %s!'
    return msg % (self._getOperation(), self.varName)
