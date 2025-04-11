"""OverloadMeta provides a metaclass for classes supporting overloaded
methods. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractMetaclass, Base
from worktoy.mcls import OverloadSpace as OSpace


class OverloadMeta(AbstractMetaclass):
  """OverloadMeta provides a metaclass for classes supporting overloaded
  methods. """

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs) -> OSpace:
    """Prepare the class namespace."""
    return OSpace(mcls, name, bases, **kwargs)
