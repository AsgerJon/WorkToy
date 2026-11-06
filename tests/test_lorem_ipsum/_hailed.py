"""
Hailed is a 'Clause' with a lead-in of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.lorem_ipsum import Clause


class Hailed(Clause):
  """
  A project brings its own lead-in by rebinding the lead-in words, and
  the first clause then opens with them. 'Hailed' opens with 'Ave
  mundi', nine characters, so its short-first threshold lies at
  fourteen.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __lead_in__ = ('Ave', 'mundi')
