"""
SkipSet is the 'ControlFlow' signal that aborts a descriptor set without
surfacing an error at the call site.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import ControlFlow


class SkipSet(ControlFlow):
  """'ControlFlow' exception that aborts a descriptor set silently.

  The 'Object.__set__' wrapper catches 'SkipSet' raised from
  'hookPreSet' and skips '__instance_set__' and 'hookOnSet'
  entirely. The caller sees no exception and no error.

  Used irresponsibly this leads to highly undefined behaviour: the
  caller cannot learn that their write was discarded. The canonical,
  recommended use case is redundant-set elision: raise 'SkipSet'
  when 'newValue' is already the value the descriptor holds. That is
  safe because the caller's intent is already satisfied. For any
  other "refuse to set" scenario, raise a proper typed exception
  that propagates.
  """
