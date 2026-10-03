"""
The 'worktoy.waitaminute.ezdata' package provides the custom exceptions
raised by the 'worktoy.ezdata' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._duplicate_error import DuplicateError
from ._extra_positional_exception import ExtraPositionalException
from ._kw_only_exception import KwargsOnlyException
from ._incomplete_field_exception import IncompleteFieldException
from ._reserved_field_error import ReservedFieldError
from ._class_field_error import ClassFieldError
from ._reserved_method_error import ReservedMethodError
from ._class_keyword_error import ClassKeywordError
from ._extra_keyword_exception import ExtraKeywordException
from ._repeated_field_exception import RepeatedFieldException
from ._reserved_attribute_error import ReservedAttributeError

__all__ = [
  'DuplicateError',
  'ExtraPositionalException',
  'KwargsOnlyException',
  'IncompleteFieldException',
  'ReservedFieldError',
  'ClassFieldError',
  'ReservedMethodError',
  'ClassKeywordError',
  'ExtraKeywordException',
  'RepeatedFieldException',
  'ReservedAttributeError',
]
