"""This files provides common type names used by the mcls package. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.mcls import AbstractNamespace

  Bases = tuple[type, ...]
  Space = AbstractNamespace
else:
  Bases = object
  Space = object
