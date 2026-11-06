"""
Reporter is a plain mixin written against the dataclass protocol.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class Reporter:
  """
  A plain base, one not built by 'EZMeta', may define the methods
  EZData generates: the optional ones it supplies win, while the
  generated reserved ones take precedence. 'Reporter' writes 'asDict'
  and '__repr__' by hand, defines '__len__' plainly, holds a property
  at 'label' that would take over a field of that name, and keeps a
  class attribute 'count' that must not count as a field value.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  count = 99

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @property
  def label(self) -> str:
    return 'property'

  def asDict(self) -> dict:
    return {'reported': True}

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __repr__(self) -> str:
    return 'Reporter!'

  def __len__(self) -> int:
    return 99
