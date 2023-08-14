"""ReadOnlyError is a custom exception raised when attempting to set a
variable that is marked as read only."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import AccessorError


class ReadOnlyError(AccessorError):
  """ReadOnlyError is a custom exception raised when attempting to set a
  variable that is marked as read only."""

  def _getOperation(self) -> str:
    """Getter-function for illegally attempted accessor function"""
    return 'setter'
