"""WorkSide - Style - LineStyleField
Descriptor for line styles used by the QPen."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.style import LineStyleSym
from workside.text import FontSym
from worktoy.fields import AbstractDescriptor


class LineStyleField(AbstractDescriptor):
  """WorkSide - Style - LineStyleField
  Descriptor for line styles used by the QPen."""

  def __init__(self, *args, **kwargs) -> None:
    self._defaultValue = LineStyleSym.normal
    self._privateVariableName = '_lineStyle'
    AbstractDescriptor.__init__(self, self._defaultValue, *args, **kwargs)

  def explicitGetter(self, obj: FontSym, cls: type) -> LineStyleSym:
    """Getter-function"""
    return getattr(obj, self._privateVariableName, None)

  def explicitSetter(self, obj: FontSym, newValue: LineStyleSym) -> None:
    """Setter-function"""
    setattr(obj, self._privateVariableName, newValue)

  def explicitDeleter(self, obj: FontSym, ) -> None:
    """Deleter-function"""
    from worktoy.waitaminute import ProtectedFieldError
    raise ProtectedFieldError(self, obj, )
