"""
'DESC' provides a reference to a descriptor in a context where the actual
descriptor class to be referenced does not yet exist.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...text import monoSpace

from . import Zeroton


class DESC(metaclass=Zeroton):
  """DESC is a token object indicating the descriptor object of the
  surrounding scope. """

  @classmethod
  def __class_str__(cls, ) -> str:
    """Required explanation of the class. """
    infoSpec = """The '%s' Zeroton is a placeholder for the descriptor 
    object of the surrounding scope. """
    return monoSpace(infoSpec % cls.__name__)
