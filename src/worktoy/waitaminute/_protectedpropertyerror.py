"""ProtectedPropertyError is a subclass of AccessorError raised when
attempting to delete a protected variable."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import AccessorError


class ProtectedPropertyError(AccessorError):
  """ProtectedPropertyError is a subclass of AccessorError raised when
  attempting to delete a protected variable."""

  def _getOperation(self) -> str:
    """Getter-function for the illegal operation"""
    return 'delete'
