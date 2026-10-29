"""
The 'worktoy.waitaminute.dispatch' package provides the custom exceptions
raised by the overload control flow.

- DispatchException
- DuplicateSignature
- TypeCastException
- UnboundCastHook
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._dispatch_exception import DispatchException
from ._duplicate_signature import DuplicateSignature
from ._type_cast_exception import TypeCastException
from ._unbound_cast_hook import UnboundCastHook

__all__ = [
  'DispatchException',
  'DuplicateSignature',
  'TypeCastException',
  'UnboundCastHook',
]
