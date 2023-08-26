"""WorkToy - Core - Signature
Enhanced alternative to GenericAlias implementing instance check."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from types import GenericAlias

from worktoy.core import ParsingClass


class MetaSignature(type):
  """Metaclass for the Signature class"""

  def __instancecheck__(cls: type, obj: object) -> bool:
    """Implements the instance check"""


class Signature(GenericAlias, ParsingClass):
  """WorkToy - Core - Signature
  Enhanced alternative to GenericAlias implementing instance check."""

  def parseGenericAlias(self, alias: GenericAlias) -> dict[str, type]:
    """Parses received alias to origin and args and returns dictionary."""

  def __init__(self, base: GenericAlias) -> None:
    ParsingClass.__init__(self, base)
    GenericAlias.__init__(self, tuple, base.__args__)
