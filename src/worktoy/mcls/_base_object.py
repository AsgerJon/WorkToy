"""BaseObject exposes the functionality of the custom metaclass
implementations in the 'worktoy' library. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import BaseMeta
from ..static import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class BaseObject(AbstractObject, metaclass=BaseMeta):
  """BaseObject exposes the functionality of the custom metaclass
  implementations in the 'worktoy' library. """
