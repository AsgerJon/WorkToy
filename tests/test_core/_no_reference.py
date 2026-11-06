"""
NoReference is a value that refuses to be reached through 'THIS'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class NoReference:
  """
  'THIS[Parent].name' refuses a name holding a value whose class sets
  '__no_this_reference__', as the dispatcher of an overloaded method
  does, since a clone would replace the dispatcher the subclass builds.
  'NoReference' is a plain stand-in for such a value.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __no_this_reference__ = True
