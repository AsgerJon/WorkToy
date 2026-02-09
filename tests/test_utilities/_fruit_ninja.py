"""
FruitNinja is an example class implementing overloading of the
'__getitem__' to facilitate 'int' and 'slice' objects.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.desc import Field
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Iterator


class FruitNinja(BaseObject):
  """
  FruitNinja is an example class implementing overloading of the
  '__getitem__' to facilitate 'int' and 'slice' objects.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __data_dict__ = ('apple', 'banana', 'cherry', 'date', 'elderberry',)

  #  Public Variables
  data = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @data.GET
  def _getData(self) -> tuple[str, ...]:
    return self.__data_dict__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __len__(self, ) -> int:
    return len(self.data)

  def __iter__(self, ) -> Iterator[str]:
    yield from self.data

  @overload(int)
  def __getitem__(self, index: int) -> str:
    if index < 0:
      return self.__getitem__(len(self) + index)
    if index < len(self):
      return self.data[index]
    infoSpec = """%s index out of range. Valid indices are up to %d, 
    but received %d!"""
    info = infoSpec % (type(self).__name__, len(self) - 1, index)
    raise IndexError(info)

  @overload(slice)
  def __getitem__(self, index: slice) -> tuple[str, ...]:
    return (*self,)[index]
