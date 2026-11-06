"""
SizedMeta is a metaclass based on 'AbstractMetaclass' that measures its
classes itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractMetaclass


class SizedMeta(AbstractMetaclass):
  """
  A metaclass ahead of 'AbstractMetaclass' in the resolution order that
  implements an operation takes it over for its classes, which then
  cannot define the class hook of that operation. 'SizedMeta' implements
  '__len__' itself, so every class it builds has length seven, and a
  body under it binding '__class_len__' is refused.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __len__(cls) -> int:
    return 7
