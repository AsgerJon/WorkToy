"""
LoggingHook is a namespace hook that records every phase it is called in.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import AbstractSpaceHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

  from worktoy.mcls import AbstractNamespace


class LoggingHook(AbstractSpaceHook):
  """
  A namespace calls its hooks at seven phases of class construction, and
  a test of that order needs a hook that only watches. 'LoggingHook'
  appends one record per call to 'log': the phase and the name, with
  the value for a read. Its 'preCompilePhase' gives the class a default
  at 'hookDefault' that the body may replace, and its 'postCompilePhase'
  writes 'hookFinal' over whatever the body bound there.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  log: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preparePhase(self, space: AbstractNamespace) -> None:
    LoggingHook.log.append(('prepare', space.getClassName()))

  def setItemPhase(self, key: str, val: Any, old: Any = None) -> bool:
    LoggingHook.log.append(('set', key))
    return False

  def getItemPhase(self, key: str, value: Any) -> None:
    LoggingHook.log.append(('get', key, value))

  def delItemPhase(self, key: str, val: Any = None) -> bool:
    LoggingHook.log.append(('del', key))
    return False

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    LoggingHook.log.append(('pre', self.space.getClassName()))
    compiledSpace['hookDefault'] = 'pre'
    return compiledSpace

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    LoggingHook.log.append(('post', self.space.getClassName()))
    compiledSpace['hookFinal'] = 'post'
    return compiledSpace

  def newClassPhase(self, cls: type) -> type:
    LoggingHook.log.append(('new', cls.__name__))
    return cls
