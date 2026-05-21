"""The 'worktoy.waitaminute.keenum' module provides custom exceptions
used by the 'worktoy.keenum' module."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._kee_box_type_error import KeeBoxTypeError
from ._kee_box_value_error import KeeBoxValueError
from ._kee_box_exception import KeeBoxException
from ._kee_name_conflict import KeeNameConflict
from ._kee_case_exception import KeeCaseException
from ._kee_duplicate import KeeDuplicate
from ._kee_flag_duplicate import KeeFlagDuplicate
from ._kee_type_exception import KeeTypeException
from ._kee_write_once_error import KeeWriteOnceError
from ._kee_resolve_error import KeeResolveError

__all__ = [
  'KeeBoxTypeError',
  'KeeBoxValueError',
  'KeeBoxException',
  'KeeNameConflict',
  'KeeCaseException',
  'KeeDuplicate',
  'KeeFlagDuplicate',
  'KeeTypeException',
  'KeeWriteOnceError',
  'KeeResolveError',
]
