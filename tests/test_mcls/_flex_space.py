"""
FlexSpace is a 'BaseSpace' declaring a 'FlexCallHook'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseSpace
from worktoy.mcls.space_hooks import FlexCallHook


class FlexSpace(BaseSpace):
  """
  No namespace of worktoy wraps its methods with 'flexCall'; a namespace
  wanting it declares the hook. 'FlexSpace' is 'BaseSpace' with a
  'FlexCallHook' declared behind the three hooks it inherits.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  flexCallHook = FlexCallHook()
