"""SecretPropertyError is a subclass of AccessorError that should be
raised if an attempt is made to access a secret private property."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import AccessorError


class SecretPropertyError(AccessorError):
  """Access to the property is restricted."""

  def _getOperation(self) -> str:
    return 'getter'
