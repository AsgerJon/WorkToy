"""
ComplexSubclass subclasses ComplexFields exposing the descriptor
functionality applied to subclasses.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import ComplexFields

if TYPE_CHECKING:  # pragma: no cover
  pass


class ComplexFieldsSubclass(ComplexFields):
  """
  ComplexSubclass subclasses ComplexFields exposing the descriptor
  functionality applied to subclasses.
  """

  def __init__(self, *args) -> None:
    """
    Initialize the ComplexSubclass instance with the given arguments.
    """
    if len(args) == 1:
      arg = complex(args[0])
      self.RE, self.IM = arg.real, arg.imag
    else:
      self.RE, self.IM, *_ = args
