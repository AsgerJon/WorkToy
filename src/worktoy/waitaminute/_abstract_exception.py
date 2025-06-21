"""AbstractException provides an abstract baseclass for custom exceptions
in the 'worktoy.waitaminute' module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import logging
from abc import abstractmethod

from ..parse import maybe

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, Self, Never


class AbstractException(Exception):
  """AbstractException provides an abstract baseclass for custom exceptions
  in the 'worktoy.waitaminute' module."""

  def __new__(*_) -> Never:
    """
    I'll do it later, promise!
    """
    raise NotImplementedError
