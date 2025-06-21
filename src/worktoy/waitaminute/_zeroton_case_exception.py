"""ZerotonCaseException is a custom exception class raised when an attempt
is made to create a Zeroton class with a name not in all upper cases. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Never


class ZerotonCaseException(ValueError):
  """ZerotonCaseException is a custom exception class raised when an attempt
  is made to create a Zeroton class with a name not in all upper cases. """

  name = _Attribute()

  def __init__(self, name: str) -> None:
    """Initialize the ZerotonCaseException with the name."""
    self.name = name
    ValueError.__init__(self, )

  def __str__(self) -> str:
    """String representation of the exception."""
    if self.name is None:
      return ValueError.__str__(self)
    infoSpec = """Zeroton class name '%s' must be in all upper cases!"""
    return infoSpec % self.name

  __repr__ = __str__
