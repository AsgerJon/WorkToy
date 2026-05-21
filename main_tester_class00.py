"""
Main tester classes
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Union, Self

desc = type(getattr(type('_', (), dict(__slots__=('_',), )), '_'))
print(desc)
