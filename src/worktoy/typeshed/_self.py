"""Self is typing.Self or similar."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self
except ImportError as importError:
  try:
    from types import ModuleType as Self
  except ImportError as importError2:
    Self = object
