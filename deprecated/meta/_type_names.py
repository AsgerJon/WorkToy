"""This file provides some common type aliases used by 'worktoy.meta'. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TypeAlias
except ImportError:
  TypeAlias = None

from typing import Union, Tuple

try:
  from typing import Callable
except ImportError:
  Callable = object
from depr.meta import AbstractNamespace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False


def functionInstance() -> None:
  pass


Function = type(functionInstance)

if TYPE_CHECKING:
  Bases: TypeAlias = Union[type, Tuple[type, ...]]
  Space: TypeAlias = Union[dict, AbstractNamespace]
else:
  Bases = object
  Space = object
