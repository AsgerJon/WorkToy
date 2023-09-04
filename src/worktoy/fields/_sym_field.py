"""WorkSide - Style - SymField
Field implementation of symbolic classes. ."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from icecream import ic

from worktoy.fields import IntField

if TYPE_CHECKING:
  from worktoy.sym import SyMeta

ic.configureOutput(includeContext=True)


class SymField(IntField, ):
  """WorkSide - Style - SymField
  Field implementation of symbolic classes."""

  def __init__(self, sym: SyMeta, defVal: Any = None,
               *args, **kwargs) -> None:
    defVal = 0 if defVal is None else defVal
    intVal = 1
    IntField.__init__(self, intVal, *args, **kwargs)
    self._defaultValue = intVal
    self._symbolicClass = sym

  def getSymClass(self) -> SyMeta:
    """Getter-function for the symbolic class."""
    return self._symbolicClass

  def sym2Int(self, symValue: Any) -> int:
    """Converts symbolic value to integer."""
    intValue = getattr(symValue, 'value', None)
    if intValue is None:
      from worktoy.waitaminute import SymbolicConversionError
      raise SymbolicConversionError(self.getSymClass(), intValue)
    return intValue

  def int2Sym(self, intValue: int) -> Any:
    """Converts integer value to symbolic value."""
    sym = self.getSymClass()
    symValue = self.getSymClass()(intValue)
    if symValue is None:
      from worktoy.waitaminute import SymbolicConversionError
      raise SymbolicConversionError(self.getSymClass(), symValue)
    return symValue

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Implementation of explicit getter."""
    value = IntField.explicitGetter(self, obj, cls)
    return self.int2Sym(value)

  def explicitSetter(self, obj: object, newValue: Any) -> None:
    """Implementation of explicit getter."""
    if isinstance(newValue, int):
      return IntField.explicitSetter(self, obj, newValue)
    return IntField.explicitSetter(self, obj, self.sym2Int(newValue))


class SymLabel(SymField):
  """WorkSide - Style - SymLabel
  Label implementation of symbolic classes with values locked at instance
  creation time."""

  def __init__(self, sym: SyMeta, intVal: int = None,
               *args, **kwargs) -> None:
    SymField.__init__(self, sym, intVal, *args, **kwargs)

  def illegalSetter(self, obj: object, newValue: object) -> None:
    """Implementation of one-time setting if value is NULL."""
    existing = SymField.explicitGetter(self, obj, self.getFieldOwner())
    if existing:
      return SymField.illegalSetter(self, obj, newValue)
    SymField.explicitSetter(self, obj, newValue)

  def getPermissionLevel(self) -> int:
    """ReadOnly, 1"""
    return 1
