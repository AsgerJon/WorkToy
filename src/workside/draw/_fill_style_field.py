"""WorkSide - Style - FillSymField
Field class for the symbolic brush style class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.style import FillStyleSym
from workside.text import FontSym
from worktoy.fields import AbstractDescriptor


class FillStyleField(AbstractDescriptor):
  """WorkSide - Style - FillSymField
  Field class for the symbolic brush style class."""

  def __init__(self, *args, **kwargs) -> None:
    self._defaultValue = FillStyleSym.blank
    self._privateVariableName = '_fillStyle'
    AbstractDescriptor.__init__(self, self._defaultValue, *args, **kwargs)

  def explicitGetter(self, obj: FontSym, cls: type) -> FillStyleSym:
    """Getter-function"""
    return getattr(obj, self._privateVariableName, None)

  def explicitSetter(self, obj: FontSym, newValue: FillStyleSym) -> None:
    """Setter-function"""
    setattr(obj, self._privateVariableName, newValue)

  def explicitDeleter(self, obj: FontSym, ) -> None:
    """Deleter-function"""
    from worktoy.waitaminute import ProtectedFieldError
    raise ProtectedFieldError(self, obj, )
