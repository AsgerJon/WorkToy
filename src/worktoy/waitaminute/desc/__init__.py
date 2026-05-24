"""The 'worktoy.waitaminute.desc' package collects the exceptions raised
by the descriptor protocol in 'worktoy.desc' and 'worktoy.core'.

Every exception here subclasses 'DescriptorException', which 'Object' uses
to recognise a descriptor-raised failure: such an exception propagates to
the caller instead of being routed to a fallback accessor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._descriptor_exception import DescriptorException
from ._access_error import AccessError
from ._protected_error import ProtectedError
from ._read_only_error import ReadOnlyError
from ._without_exception import WithoutException
from ._write_once_error import WriteOnceError

__all__ = [
  'DescriptorException',
  'AccessError',
  'ReadOnlyError',
  'ProtectedError',
  'WithoutException',
  'WriteOnceError',
]
