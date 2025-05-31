"""THIS is the token object indicating a class before it is created. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...text import monoSpace

from . import Zeroton

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class THIS(metaclass=Zeroton):
  """THIS is the token object indicating a class before it is created. """

  @classmethod
  def __class_str__(cls, ) -> str:
    """Return the class name of the class."""
    infoSpec = """The '%s' Zeroton indicates a placeholder for a class not 
    yet created allowing it to be referenced before creation. """
    return monoSpace(infoSpec % cls.__name__)
