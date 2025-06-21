"""AbstractException provides an abstract baseclass for custom exceptions
in the 'worktoy.waitaminute' module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import logging
from abc import abstractmethod

from ..parse import maybe

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, Never


class AbstractException(Exception):
  """AbstractException provides an abstract baseclass for custom exceptions
  in the 'worktoy.waitaminute' module."""

  def __new__(*_) -> Never:
    """
    I'll do it later, promise!
    """
    raise NotImplementedError
