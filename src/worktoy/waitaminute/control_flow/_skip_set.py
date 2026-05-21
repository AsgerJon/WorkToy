"""
SkipSet is a 'ControlFlow' exception that aborts a descriptor's set
operation without surfacing an error at the call site. The
surrounding '__set__' machinery catches it and silently skips both
'__instance_set__' and 'hookOnSet'.

Used irresponsibly this leads to highly undefined behaviour. The
caller has no way to learn that their write was discarded, so any
post-condition that depends on the new value taking effect will be
silently violated.

The canonical and recommended use case is redundant-set elision:
'hookPreSet' raises 'SkipSet' when 'newValue' is already the value
the descriptor holds, so the downstream work ('__instance_set__',
notifications, persistence, 'hookOnSet') is skipped. This is safe
because the caller's intent ('x == newValue') is already satisfied
and no observable state changes.

Do not use 'SkipSet' for validation rejection, write-once
protection, or any other "refuse to set" scenario where the caller
should learn that their write was discarded. For those, raise a
proper typed exception that propagates.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import ControlFlow

if TYPE_CHECKING:  # pragma: no cover
  pass


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
