"""TestAbstractNamespace - Test the AbstractNamespace class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from unittest import TestCase

from worktoy.mcls import AbstractNamespace, Base, Space, AbstractMetaclass

if TYPE_CHECKING:
  from typing import Any, Callable, Self
