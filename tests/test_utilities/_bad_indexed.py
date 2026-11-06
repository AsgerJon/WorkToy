"""
BadIndexed is a class holding a '__index__' that is not callable.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class BadIndexed:
  """
  'ValidSlice' refuses a slice component whose type has a '__index__'
  that cannot be called. 'BadIndexed' holds an integer at that name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __index__ = 42
