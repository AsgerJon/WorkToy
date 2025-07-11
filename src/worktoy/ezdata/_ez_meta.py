"""EZMeta provides the metaclass for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic

from . import EZDesc
from ..mcls import AbstractMetaclass, Base, BaseMeta
from ..ezdata import EZSpace

if TYPE_CHECKING:  # pragma: no cover
  pass

ic.configureOutput(includeContext=True)


class EZMeta(BaseMeta):
  """EZMeta provides the metaclass for the EZData class."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  isFrozen = EZDesc('frozen', bool, False)
  isOrdered = EZDesc('order', bool, False)
  requireKwargs = EZDesc('kw_only', bool, False)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs: dict) -> EZSpace:
    """Prepare the class namespace."""
    return EZSpace(mcls, name, bases, **kwargs)

  def __len__(cls) -> int:
    """Return the number of class variables."""
    return len(getattr(cls, '__slots__', ()))
