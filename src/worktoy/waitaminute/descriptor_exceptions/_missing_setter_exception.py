"""MissingSetterException is a subclass of MissingAccessorException that is
raised when the get accessor is missing from the descriptor."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

import worktoy.waitaminute.descriptor_exceptions as dex


class MissingSetterException(dex.MissingAccessorException):
  """MissingSetterException is a subclass of MissingAccessorException that is
  raised when the get accessor is missing from the descriptor."""

  def __init__(self, descriptor: object) -> None:
    setterFunc = getattr(descriptor, '__set__', )
    dex.MissingAccessorException.__init__(self, descriptor, setterFunc)
