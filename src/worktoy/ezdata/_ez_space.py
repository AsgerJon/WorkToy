"""EZSpace provides the namespace object class for the EZMetaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastSpace
from worktoy.desc import ExplicitBox, AttriBox
from worktoy.meta import CallMeMaybe, AbstractNamespace


class EZSpace(AbstractNamespace):
  """EZSpace provides the namespace object class for the EZMetaclass."""

  def __setitem__(self, key: str, value: object) -> None:
    if isinstance(value, AttriBox):
      return AbstractNamespace.__setitem__(self, key, value)
