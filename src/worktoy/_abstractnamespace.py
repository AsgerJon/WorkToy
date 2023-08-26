"""WorkToy - AbstractNameSpace
The baseclass for namespace classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.core import ParsingClass, Items, Values, Keys


class AbstractNameSpace(ParsingClass):
  """Namespace class for Struc class"""

  def __init__(self, *__, **_) -> None:
    ParsingClass.__init__(self, *__, **_)
    self._contents = {}
    self._entries = []
    self._iterContents = None

  @abstractmethod
  def applyTransform(self, key: str) -> object:
    """Applies transform to one key at a time"""

  def __getitem__(self, key: str, *args, **kwargs) -> object:
    """Item retrieval."""
    return self.applyTransform(key)

  def __setitem__(self, key: str, val: object, *args, **kwargs) -> None:
    """Item setting."""
    self._contents[key] = val

  def __delitem__(self, key: str) -> None:
    """Item deleter."""
    del self._contents[key]

  def __contains__(self, key: str) -> bool:
    """Membership test"""
    return True if key in self.keys() else False

  def keys(self, ) -> Keys:
    """Implementation of keys"""
    return self._contents.keys()

  def values(self, ) -> Values:
    """Implementation of values"""
    return [self[key] for key in self.keys()]

  def items(self, ) -> Items:
    """Implementation of items"""
    return [(key, self[key]) for key in self.keys()]

  def __iter__(self, ) -> AbstractNameSpace:
    """Implementation of iteration"""
    self._resetIterContents()
    return self

  def __next__(self) -> str:
    """Implementation of iteration"""
    try:
      return self._getIterContents().pop(0)
    except IndexError:
      self._iterContents = None
      raise StopIteration

  def _resetIterContents(self) -> None:
    """Resets the iteration"""
    self._iterContents = [k for k in self._contents.keys()]

  def _getIterContents(self) -> list:
    """Returns the iteration content"""
    return self._iterContents
