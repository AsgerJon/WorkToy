"""
Config is a worktoy class with write-once attributes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FixBox
from worktoy.mcls import BaseObject


class Config(BaseObject):
  """
  A 'FixBox' is set once per instance and never changes after, keeping
  everything an 'AttriBox' gives. 'Config' holds a port and a host, with
  a callback before every write recorded in 'attempts'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  attempts: list = []

  #  Public Variables
  port = FixBox[int](8080)
  host = FixBox[str]('localhost')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @port.preSet
  def _attempt(self, value: int) -> None:
    Config.attempts.append(value)
