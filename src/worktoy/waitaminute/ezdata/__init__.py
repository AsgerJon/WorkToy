"""
The 'worktoy.waitaminute.ez' module provides custom exception classes used
by the 'worktoy.ezdata' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._duplicate_error import DuplicateError
from ._extra_positional_exception import ExtraPositionalException
from ._kw_only_exception import KwargsOnlyException
from ._incomplete_field_exception import IncompleteFieldException
from ._reserved_field_error import ReservedFieldError

__all__ = [
  'DuplicateError',
  'ExtraPositionalException',
  'KwargsOnlyException',
  'IncompleteFieldException',
  'ReservedFieldError',
]
