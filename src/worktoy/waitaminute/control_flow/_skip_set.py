"""
SkipSet is a 'ControlFlow' exception that can stop a setter without
propagating an error. For example, if a setter would set a value not
different from the existing value.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import ControlFlow

if TYPE_CHECKING:  # pragma: no cover
  pass


class SkipSet(ControlFlow):
  """
  SkipSet is a 'ControlFlow' exception that can stop a setter without
  propagating an error. For example, if a setter would set a value not
  different from the existing value.
  """
