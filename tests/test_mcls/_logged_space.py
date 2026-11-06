"""
LoggedSpace is a namespace class declaring a 'LoggingHook'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace

from . import LoggingHook


class LoggedSpace(AbstractNamespace):
  """
  A namespace class gains a hook by declaring it in its body, behind the
  two hooks every namespace has. 'LoggedSpace' declares a 'LoggingHook'
  and nothing else.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  loggingHook = LoggingHook()
