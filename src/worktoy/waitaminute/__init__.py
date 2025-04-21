"""The 'worktoy.waitaminute' module provides custom exception classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._cast_mismatch import CastMismatch
from ._dispatch_exception import DispatchException
from ._sig_mismatch import SigMismatch
from ._resolve_exception import ResolveException
from ._missing_variable import MissingVariable
from ._variable_not_none import VariableNotNone
from ._questionable_syntax import QuestionableSyntax
from ._read_only_error import ReadOnlyError
from ._reserved_name import ReservedName
from ._hook_exception import HookException
from ._hash_mismatch import HashMismatch
from ._missing_object import MissingObject
from ._unrecognized_member import UnrecognizedMember
from ._write_once_error import WriteOnceError
from ._startup_exception import StartupException
from ._subclass_exception import SubclassException
from ._protected_error import ProtectedError

__all__ = [
    'CastMismatch',
    'DispatchException',
    'SigMismatch',
    'ResolveException',
    'MissingVariable',
    'VariableNotNone',
    'QuestionableSyntax',
    'ReadOnlyError',
    'ReservedName',
    'HookException',
    'HashMismatch',
    'MissingObject',
    'UnrecognizedMember',
    'WriteOnceError',
    'StartupException',
    'SubclassException',
    'ProtectedError'
]
