"""
DuplicateSlot is a custom exception raised to indicate that a class was
defined with a key that is both in the '__slots__' and the class body.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type


class DuplicateSlot(TypeError):
  """DuplicateSlot is a custom exception raised to indicate that a class was
  defined with a key that is both in the '__slots__' and the class body.
  """

  __slots__ = ('space', 'key')

  def __init__(self, space: dict, key: str, ) -> None:
    """Initialize the DuplicateSlot with the class and key."""
    self.space = space
    self.key = key
    TypeError.__init__(self, )

  def __str__(self, ) -> str:
    """
    Return the string representation of the DuplicateSlot object.
    """
    infoSpec = """The class body of '%s' contains '%s' as both a key and a 
    slot!"""
    clsName = getattr(self.space, '__class_name__', )
    info = infoSpec % (clsName, self.key)
    from worktoy.utilities import textFmt
    return textFmt(info)

  __repr__ = __str__
