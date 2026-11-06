"""
LoudMeta is a metaclass based on 'MetaType' with a text of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType


class LoudMeta(MetaType):
  """
  The defaults of 'AbstractMetaclass' hand over with 'super()', so a
  metaclass based on 'MetaType' listed behind it takes part. 'LoudMeta'
  writes its classes as 'LOUD' followed by the name, in 'str' and in
  'repr'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(cls) -> str:
    return 'LOUD %s' % cls.__name__

  __repr__ = __str__
