"""
SubNotated subclasses AnnotatedClass to test if EZData correctly interprets
slot as annotations when inherited.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import AnnotatedClass

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any
