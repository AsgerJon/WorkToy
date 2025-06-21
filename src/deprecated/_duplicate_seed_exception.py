"""
DuplicateSeedException is a custom exception raised by the KingDice class
when receiving duplicate seeds.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

try:
  from typing import TYPE_CHECKING, Any
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.worktest import KingDice


class DuplicateSeedException(Exception):
  """
  SeedException is a custom exception raised by the KingDice class when
  receiving duplicate seeds.
  """

  king = _Attribute()
  oldSeed = _Attribute()
  newSeed = _Attribute()

  def __init__(self, king: KingDice, oldSeed: int, newSeed: int) -> None:
    """
    Initializes the DuplicateSeedException with the KingDice instance and
    the old and new seeds.

    Args:
        king (KingDice): The KingDice instance that raised the exception.
        oldSeed (int): The old seed that caused the exception.
        newSeed (int): The new seed that caused the exception.
    """
    self.king = king
    self.oldSeed = oldSeed
    self.newSeed = newSeed
    fieldName = getattr(self.king, '__field_name__')
    fieldOwner = getattr(self.king, '__field_owner__')
    if fieldName is None or fieldOwner is None:
      infoSpec = """Tried changing the seed of existing '%s%s%s' object from 
      %d to %d. '%s' objects are expected to have unchanging seeds.  """
      ownerName = ''
      fieldName = ''
    else:
      infoSpec = """Tried changing the seed of existing '%s' object at 
      '%s.%s' from %d to %d. '%s' objects are expected to have unchanging 
      seeds. """
      ownerName = fieldOwner.__name__
    clsName = type(self.king).__name__
    info = infoSpec % (
        clsName, ownerName, fieldName, oldSeed, newSeed, clsName
    )
    Exception.__init__(self, monoSpace(info))

  def __eq__(self, other: Any) -> bool:
    """
    Checks if the current instance is equal to another object.

    Args:
        other (Any): The object to compare with.

    Returns:
        bool: True if the objects are equal, False otherwise.
    """
    if not isinstance(other, DuplicateSeedException):
      return False
    if self.king != other.king:
      return False
    if self.oldSeed != other.oldSeed:
      return False
    if self.newSeed != other.newSeed:
      return False
    return True
