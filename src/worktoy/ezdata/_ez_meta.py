"""EZMeta provides the metaclass for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..mcls import AbstractMetaclass, Base
from ..ezdata import EZSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class EZMeta(AbstractMetaclass):
  """EZMeta provides the metaclass for the EZData class."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs: dict) -> EZSpace:
    """Prepare the class namespace."""
    return EZSpace(mcls, name, bases, **kwargs)
