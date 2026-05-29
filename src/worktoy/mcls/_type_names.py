"""
This file provides the common type names used by the 'mcls' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from worktoy.mcls import AbstractNamespace

  Space = AbstractNamespace
  Spaces = tuple[AbstractNamespace, ...]
  Base = tuple[type, ...]
  Types = tuple[type, ...]

else:
  Space = object
  Spaces = tuple
  Base = tuple
  Types = tuple
