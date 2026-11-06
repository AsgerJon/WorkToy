"""
ClaimedSpace is a namespace class adding three hooks to 'LoggedSpace'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import LoggedSpace, ClaimingHook, RefusingHook, SwappingHook


class ClaimedSpace(LoggedSpace):
  """
  The hooks of a namespace class run in a fixed order: those its bases
  declared first, then its own in declaration order. 'ClaimedSpace'
  adds a 'ClaimingHook', a 'RefusingHook' and a 'SwappingHook' behind
  the 'LoggingHook' of 'LoggedSpace'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  claimingHook = ClaimingHook()
  refusingHook = RefusingHook()
  swappingHook = SwappingHook()
