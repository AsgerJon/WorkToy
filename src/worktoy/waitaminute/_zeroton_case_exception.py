"""ZerotonCaseException is a custom exception class raised when an attempt
is made to create a Zeroton class with a name not in all upper cases. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Never


class ZerotonCaseException(ValueError):
  """ZerotonCaseException is a custom exception class raised when an attempt
  is made to create a Zeroton class with a name not in all upper cases. """

  name = _Attribute()

  def __init__(self, name: str) -> None:
    """Initialize the ZerotonCaseException with the name."""
    self.name = name
    infoSpec = """Zeroton class name '%s' must be in all upper cases!"""
    info = infoSpec % name
    ValueError.__init__(self, info)
