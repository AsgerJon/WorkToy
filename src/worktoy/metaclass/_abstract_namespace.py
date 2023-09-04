"""WorkToy - MetaClass - AbstractNameSpace
The AbstractNameSpace class provides a class with the minimal
functionality required."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Keys, Items, Values, Bases
from worktoy.metaclass import MetaNameSpace


class AbstractNameSpace(dict, metaclass=MetaNameSpace):
  """WorkToy - MetaClass - AbstractNameSpace
  The AbstractNameSpace class provides a class with the minimal
  functionality required."""

  def __init__(self, name: str = None, bases: Bases = None,
               **kwargs) -> None:
    super().__init__()
    self._name = name
    self._bases = bases
    self._kwargs = kwargs
    self._latestErrorGet = None
    self._latestErrorSet = None
    self._log = []
    dict.__setitem__(self, '__name__', '\n |> WorkToy <| SYM\n')

  def __setitem__(self, key: str, val: object, *args, **kwargs) -> None:
    self._log.append(['set', key, val, ])
    dict.__setitem__(self, key, val, )

  def __getitem__(self, key: str, *args, **kwargs) -> object:
    try:
      val = dict.__getitem__(self, key)
      self._recordLog(['get', key, val, ])
      return val
    except KeyError as e:
      self._recordLog(['getError', key, e, ])
      raise e

  def __delitem__(self, key: str) -> None:
    dict.__delitem__(self, key)

  def __contains__(self, key: str) -> bool:
    val = dict.__contains__(self, key)
    return True if val else False

  def keys(self) -> Keys:
    """Implementation of keys"""
    return dict.keys(self)

  def items(self) -> Items:
    """Implementation of keys"""
    return dict.items(self)

  def values(self) -> Values:
    """Implementation of keys"""
    return dict.values(self)

  def getName(self) -> str:
    """Getter-function for name of created class"""
    return self._name

  def getBases(self) -> Bases:
    """Getter-function for name of bases"""
    return self._bases

  def getKwargs(self) -> dict:
    """Getter-function for the keyword arguments"""
    return self._kwargs

  def _recordLog(self, entry: list) -> None:
    """Records the log"""
    self._log.append(entry)

  def getLog(self) -> list:
    """Getter-function for the log"""
    return self._log
