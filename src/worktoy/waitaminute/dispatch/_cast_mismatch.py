"""
CastMismatch is a custom exception raised to indicate that a 'TypeSig'
object has failed to cast a collection of arguments to itself.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import HashMismatch

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class CastMismatch(HashMismatch):
  """
  CastMismatch is a custom exception raised to indicate that a 'TypeSig'
  object has failed to cast a collection of arguments to itself.
  """
