"""WorkSide - Style - FontWeightField
Symbolic field representing the text weight."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.style import FontWeightSym
from workside.text import FontSym
from worktoy.fields import AbstractDescriptor


class FontWeightField(AbstractDescriptor):
  """WorkSide - Style - FontWeightField
  Symbolic field representing the text weight."""

  def __init__(self, *args, **kwargs) -> None:
    self._defaultValue = FontWeightSym.normal
    self._privateVariableName = '_fontWeight'
    AbstractDescriptor.__init__(self, self._defaultValue, *args, **kwargs)

  def explicitGetter(self, obj: FontSym, cls: type) -> FontWeightSym:
    """Getter-function"""
    return getattr(obj, self._privateVariableName, None)

  def explicitSetter(self, obj: FontSym, newValue: FontWeightSym) -> None:
    """Setter-function"""
    setattr(obj, self._privateVariableName, newValue)

  def explicitDeleter(self, obj: FontSym, ) -> None:
    """Deleter-function"""
    from worktoy.waitaminute import ProtectedFieldError
    raise ProtectedFieldError(self, obj, )
