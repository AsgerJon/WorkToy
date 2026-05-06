"""
The 'maybe' function returns the first value that is not 'None'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, overload

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Union, Optional

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  @overload
  def maybe(a0: T, a1: T) -> T: ...
  @overload
  def maybe(a0: T, a1: None) -> T: ...
  # @formatter:on


def maybe(*args) -> T:
  """
  Returns the first argument that is not None.
  """
  for arg in args:
    if arg is not None:
      return arg
  return None
