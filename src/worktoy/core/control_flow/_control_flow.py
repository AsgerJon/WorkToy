"""
ControlFlow is a special base exception class for use in control flow.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import MetaFlow


class ControlFlow(Exception, metaclass=MetaFlow, _root=True):
  """
  Control-flow signals need one root, so 'except ControlFlow' catches
  every signal, and so a signal is never mistaken for an error: it is
  not a 'WorkToyException'.

  Implementation
  --------------

  'ControlFlow' is declared with '_root=True'. Every other signal is a
  subclass of it, with a body limited to a docstring, '__str__' and
  '__repr__'.
  """
