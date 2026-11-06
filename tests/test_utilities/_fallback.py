"""
Fallback is a class that says it was defined in a module no file stands
behind, for the tests of 'Directory'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import Directory


class Fallback:
  """
  A class defined in the REPL or under 'exec' has a module without a
  '__file__', and 'Directory' must refuse to report a directory for it.
  'Fallback' says it was defined in 'fallback_module', a name the test
  registers in 'sys.modules' as a bare module, or leaves unregistered.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __module__ = 'fallback_module'

  #  Public Variables
  here = Directory()
