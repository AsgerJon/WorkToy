"""WorkSide - Style - Font
Implementing descriptor access to text values."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from workside.text import STYLECLASS
from worktoy.fields import AbstractDescriptor


class FontField(AbstractDescriptor):
  """WorkSide - Style - Font
  Implementing descriptor access to text values."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._fieldName = None
    self._ownerClass = STYLECLASS  # The style. This descriptor provides the
    # FONT class. Then its descriptors point to family size and weight.

  def getPermissionLevel(self) -> int:
    """ReadOnly, 1"""
    return 1

  def explicitGetter(self, obj: Any, cls: type) -> Any:
    """Getter-function"""
    return getattr(obj, '_FONT', None)

  def explicitSetter(self, obj: Any, newValue: Any) -> None:
    """Setter-function"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError(self, obj, newValue)

  def explicitDeleter(self, obj: Any, ) -> None:
    """Setter-function"""
    from worktoy.waitaminute import ProtectedFieldError
    raise ProtectedFieldError(self, obj, )
