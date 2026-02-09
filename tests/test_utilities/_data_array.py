"""
DataArray overloads '__getitem__' for 'int', 'str' and 'slice' objects.
All entries must be 'str' objects. The 'str' overload first looks for an
entry beginning with the key, next for an entry containing the key before
raising 'KeyError'. The 'int' overload finds the entry at the given index,
supporting negative indices, and raises 'IndexError' if the index is out
of range. The 'slice' overload returns a tuple of entries at the given
slice indices.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator


class DataArray(BaseObject):
  """
  DataArray overloads '__getitem__' for 'int', 'str' and 'slice' objects.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __data_bucket__ = None

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getDataBucket(self, ) -> tuple[Any, ...]:
    return maybe(self.__data_bucket__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addItem(self, item: Any, ) -> None:
    existing = self._getDataBucket()
    self.__data_bucket__ = (*existing, item)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[str]:
    yield from self._getDataBucket()

  def __len__(self, ) -> int:
    return len(maybe(self.__data_bucket__, ()))

  @overload(int)
  def __getitem__(self, index: int) -> Any:
    if index < len(self):
      return (*self,)[index % len(self)]
    raise IndexError(index)

  def _keyStarts(self, key: str) -> str:
    for item in self:
      if str(item).startswith(key):
        return item
    raise KeyError(key)

  def _keyIn(self, key: str) -> str:
    for item in self:
      if key in str(item):
        return item
    raise KeyError(key)

  def _keyNoCase(self, key: str) -> str:
    lowerKey = key.lower()
    for item in self:
      if lowerKey in str(item).lower():
        return item
    raise KeyError(key)

  @overload(str)
  def __getitem__(self, key: str) -> Any:
    resolvers = self._keyStarts, self._keyIn, self._keyNoCase
    for resolver in resolvers:
      try:
        value = resolver(key)  # noqa stfu
      except KeyError:
        continue
      else:
        break
    else:
      raise KeyError(key)
    return value

  @overload(slice)
  def __getitem__(self, index: slice) -> tuple[Any, ...]:
    return (*self,)[index]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, ) -> None:
    for item in args:
      self._addItem(item)

  append = _addItem
