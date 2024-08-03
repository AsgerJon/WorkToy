"""The EZMeta class provides the metaclass for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZSpace
from worktoy.meta import BaseMetaclass, Bases


class EZMeta(BaseMetaclass):
  """The EZMeta class provides the metaclass for the EZData class."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> EZSpace:
    return EZSpace(mcls, name, bases, **kwargs)
