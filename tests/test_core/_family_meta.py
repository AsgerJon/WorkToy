"""
FamilyMeta is a sentinel metaclass of a project, based on 'SentinelMeta'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import SentinelMeta


class FamilyMeta(SentinelMeta):
  """
  A project may build a family of sentinels that carry behaviour on a
  metaclass of its own, and that family must share the one registry, or
  two families could hold one name between them. 'FamilyMeta' adds a
  class method and nothing else.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def describe(cls) -> str:
    return 'family member %s' % cls.__name__
