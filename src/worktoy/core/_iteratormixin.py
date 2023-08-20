"""IteratorMixin provides subclasses with iteration. The class has one
abstract method that must be implemented by subclasses: _resetIterContents
This method should return a list of elements subject to iteration. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.core import Bedrock


class IteratorMixin(Bedrock):
  """IteratorMixin provides subclasses with iteration. The class has one
  abstract method that must be implemented by subclasses: _resetIterContents
  This method should return a list of elements subject to iteration. """

  @abstractmethod
  def _resetIterContents(self) -> list[object]:
    """Subclasses must implement this method to return the elements for
    iteration."""

  def _getIterContents(self) -> list[object]:
    """Getter-function for the elements for iteration."""
    if getattr(self, '_iterContents', None) is None:
      setattr(self, '_iterContents', None)
    if getattr(self, '_iterContents', None) is None:
      self._iterContents = reversed(self._resetIterContents())
    return getattr(self, '_iterContents', None)

  def __iter__(self, ) -> object:
    """Implementation of iteration"""
    self._resetIterContents()
    return self

  def __next__(self, ) -> object:
    """Implementation of iteration"""
    try:
      return self._getIterContents().pop()
    except IndexError:
      raise StopIteration
