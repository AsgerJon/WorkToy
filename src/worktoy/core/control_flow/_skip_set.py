"""
SkipSet is the 'ControlFlow' signal that aborts a descriptor set without
surfacing an error at the call site.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import ControlFlow


class SkipSet(ControlFlow):
  """
  A descriptor sometimes receives a write it has nothing to do for, most
  often the value it already holds. It needs a way to end the write
  there, without the notifications of a completed write and without an
  error at the line that assigned.

  Implementation
  --------------

  'Object.__set__' catches 'SkipSet' raised from 'hookPreSet', and then
  calls neither '__instance_set__' nor 'hookOnSet'. The caller cannot
  learn that the write was discarded, so 'SkipSet' is safe only where
  the intent of the caller is met already, as for a redundant write. A
  write refused for any other reason calls for a typed exception that
  reaches the caller.
  """
