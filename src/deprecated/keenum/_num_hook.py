"""NumHook subclasses AbstractHook and provides a hook for instances of
NUM. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..text import typeMsg
from ..waitaminute import ReservedName
from ..mcls import FunctionType as Func
from ..mcls.hooks import AbstractHook
from . import NUM

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any
  from worktoy.keenum import NumSpace as NSpace


class NumHook(AbstractHook):
  """NumHook subclasses AbstractHook and provides a hook for instances of
  NUM. """

  @staticmethod
  def _getReservedNames() -> list[str]:
    """Get the reserved names for the enumeration."""
    return [
        '__init__',
        '__bool__',
        '__str__',
        '__repr__',
        '__eq__',
        '__get__',
        '__set__',
        '__delete__',
    ]

  def setItemHook(self, key: str, value: Any, oldValue: Any, ) -> bool:
    """The setItemHook method is called when an item is set in the
    enumeration."""
    if key in self._getReservedNames():
      if not callable(value):
        raise TypeError(typeMsg(key, value, Func))
      if getattr(value, '__is_root__', None) is None:
        raise ReservedName(key, )
      if self.space.getClassName() != 'KeeNum':
        raise ReservedName(key, )
      return False
    if isinstance(value, NUM):
      return self.space.addNum(key, value)
    return False

  def postCompileHook(self, compiledSpace: dict) -> dict:
    """The postCompileHook method is called after the namespace is
    compiled."""
    compiledSpace['__member_objects__'] = []
    compiledSpace['__allow_instantiation__'] = True
    return compiledSpace
