"""
Ledger is a worktoy class measured, searched, subscripted and asked for
missing attributes through its class hooks.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Ledger(BaseObject):
  """
  A class behaving as a mapping defines '__class_len__',
  '__class_contains__', '__class_setitem__' and '__class_delitem__',
  and a class answering for attributes it does not have defines
  '__class_getattr__'. 'Ledger' keeps its entries in 'entries', answers
  a missing public name with the entry of that name or a tagged tuple,
  and leaves every private name missing, so the tools inspecting the
  module see nothing. Without '__class_bool__', its truth follows its
  length.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  entries: dict = {}

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CLASS HOOKS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_len__(cls) -> int:
    return len(cls.entries)

  @classmethod
  def __class_contains__(cls, item: Any) -> bool:
    return True if item in cls.entries else False

  @classmethod
  def __class_setitem__(cls, key: Any, value: Any) -> None:
    cls.entries[key] = value

  @classmethod
  def __class_delitem__(cls, key: Any) -> None:
    del cls.entries[key]

  @classmethod
  def __class_getattr__(cls, name: str) -> Any:
    if name.startswith('_'):
      raise AttributeError(name)
    if name in cls.entries:
      return cls.entries[name]
    return 'ledger', name
