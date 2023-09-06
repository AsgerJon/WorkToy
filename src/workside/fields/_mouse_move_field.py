"""WorkSide - Fields - MouseMoveField"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any

from PySide6.QtGui import QMouseEvent

from worktoy.fields import AbstractField


class MouseMoveField(AbstractField):
  """WorkToy - Fields
  Implementation of descriptors as fields."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)

  def explicitSetter(self, obj: object, newValue: object) -> Never:
    """Disabled"""
    from worktoy.waitaminute import DisabledFunctionError
    raise DisabledFunctionError(AbstractField, MouseMoveField)

  def explicitDeleter(self, *_) -> Never:
    """Disabled"""
    from worktoy.waitaminute import DisabledFunctionError
    raise DisabledFunctionError(AbstractField, MouseMoveField)

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Collects the mouse movement events."""

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Stolen method!"""

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Stolen method!"""

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Stolen method!"""

  def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    """Stolen method!"""

  def enterEvent(self, event: QMouseEvent) -> None:
    """Stolen method!"""

  def leaveEvent(self, event: QMouseEvent) -> None:
    """Stolen method!"""
