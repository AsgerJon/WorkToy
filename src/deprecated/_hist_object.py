"""
HistObject drops in for 'BaseObject' but with the namespace based on
'HistDict' rather than directly on 'dict'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from test_static import HistMetaclass
from worktoy.attr import _FieldProperties

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any, Callable


class HistObject(AbstractObject, metaclass=HistMetaclass):
  pass
