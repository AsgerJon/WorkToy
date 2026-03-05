"""
ControlFlow is a special base exception class for use in control flow.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import MetaFlow

if TYPE_CHECKING:  # pragma: no cover
  pass


class ControlFlow(Exception, metaclass=MetaFlow, _root=True):
  """
  ControlFlow is a special base exception class for use in control flow.
  """
