"""
ComplexSubclass subclasses ComplexFields exposing the descriptor
functionality applied to subclasses.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import ComplexFields


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
