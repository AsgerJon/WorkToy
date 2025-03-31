"""MissingDeleterException is a subclass of MissingAccessorException that is
raised when the get accessor is missing from the descriptor."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

import worktoy.waitaminute.descriptor_exceptions as dex


class MissingDeleterException(dex.MissingAccessorException):
  """MissingDeleterException is a subclass of MissingAccessorException
  that is raised when the get accessor is missing from the descriptor."""

  def __init__(self, descriptor: object) -> None:
    deleterFunc = getattr(descriptor, '__delete__', )
    dex.MissingAccessorException.__init__(self, descriptor, deleterFunc)
