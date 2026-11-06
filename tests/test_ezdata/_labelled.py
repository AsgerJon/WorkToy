"""
Labelled is a dataclass listing the plain mixin 'Reporter' first.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData

from . import Reporter


class Labelled(Reporter, EZData):
  """
  The field 'label' clashes with the property of 'Reporter' and so
  receives an 'EZStore'; the field 'count' shares its name with a class
  attribute of 'Reporter' that must not stand in for a value. 'asDict'
  and '__repr__' come from 'Reporter', the generated '__len__' wins.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fields
  label = 'tag'
  count = 1
