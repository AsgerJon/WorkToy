"""
ControlFlow is a special base exception class for use in control flow.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import MetaFlow


class ControlFlow(Exception, metaclass=MetaFlow, _root=True):
  """
  ControlFlow is a special base exception class for use in control flow.
  """
