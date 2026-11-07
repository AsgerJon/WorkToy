"""
SlowSpace is a namespace class declaring a 'SlowSpaceHook'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace

from . import SlowSpaceHook


class SlowSpace(AbstractNamespace):
  """
  The hook that tells a foreign namespace from its own needs a namespace
  class to be declared in. 'SlowSpace' declares a 'SlowSpaceHook' and
  nothing else.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  slowHook = SlowSpaceHook()
