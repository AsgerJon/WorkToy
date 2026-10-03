"""
ControlFlow is a special base exception class for use in control flow.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import NoPickle
from . import MetaFlow


class ControlFlow(NoPickle, Exception, metaclass=MetaFlow, _root=True):
  """
  ControlFlow is a special base exception class for use in control flow.
  """
