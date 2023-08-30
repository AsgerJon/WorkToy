"""WorkToy - Fields - ConstLabelField
Provides a field of constant value."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import LabelField


class ConstLabelField(LabelField):
  """WorkToy - Fields - ConstLabelField
  Provides a field of constant value."""

  def __init__(self, text: str = None, *args, **kwargs) -> None:
    if text is None:
      raise ValueError('ConstLabelField requires a text argument!')
    LabelField.__init__(self, *args, **kwargs)
    self._defaultValue = text

  def __str__(self) -> str:
    """String Representation"""
    return 'Field: %s' % self._defaultValue

  def __repr__(self, ) -> str:
    return '%s(%s)' % (self.__class__.__qualname__, self._defaultValue)
