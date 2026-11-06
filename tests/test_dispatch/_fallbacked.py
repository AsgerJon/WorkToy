"""
Fallbacked is a worktoy class with a fallback and a finalizer on one name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Fallbacked(BaseObject):
  """
  A call no declaration accepts may go to a fallback, and a finalizer
  runs after every call of the name. 'Fallbacked' takes an integer,
  falls back for anything else, and records every call in 'log'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  log: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def take(self, n: int) -> tuple:
    return 'int', n

  @overload.fallback
  def take(self, *args, **kwargs) -> tuple:
    return 'fallback', args, kwargs

  @overload.finalize
  def take(self, *args, **kwargs) -> None:
    Fallbacked.log.append(('final', args))
