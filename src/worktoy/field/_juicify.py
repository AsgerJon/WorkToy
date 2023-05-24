"""Juicify is a class of class decorators."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from abc import abstractmethod
from typing import Any, NoReturn

from worktoy.core import CallMeMaybe, extractArg, maybe
from worktoy.field import Field, MetaJuice
from worktoy.stringtools import stringList


@Field('activeKeys', allowSet=False, type_=list, defVal=[])
@Field('allKeys', allowSet=False, type_=list, defVal=[])
@Field('docs', allowSet=False, type_=str)
@Field('name', allowSet=False, defVal='juiced')
class Juicify(MetaJuice):
  """Juicify is a class of class decorators.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    nameKeys = stringList('name, id, variableName, varName')
    _name, a, k = extractArg(str, nameKeys, *args, **kwargs)
    self.name = maybe(_name, self.name, 'lol')
    self._clearActiveKeys()

  def _loadDocs(self) -> NoReturn:
    """Loads the docs"""
    with open('_config.inf', 'r', encoding='utf-8') as f:
      self._docs = f.read()

  def _collectAllKeys(self) -> NoReturn:
    """Collects every factory key defined on the class"""

  def _clearActiveKeys(self) -> NoReturn:
    """Flushes the list of mainKeys"""
    while self.activeKeys:
      self.activeKeys.pop()

  def __call__(self, cls: type) -> type:
    """This method should not be subclassed, instead subclass the
    _decorate method which this method invokes"""
    return self._decorate(cls)

  def _compileMethods(self) -> CallMeMaybe:
    """This method assembles the methods to be combined into the
    decorator."""
