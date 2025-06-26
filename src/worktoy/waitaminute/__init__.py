"""The 'worktoy.waitaminute' module provides custom exception classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._attribute import _Attribute
from ._access_error import AccessError
from ._attribute_error_factory import attributeErrorFactory
from ._zeroton_case_exception import ZerotonCaseException
from ._metaclass_exception import MetaclassException
from ._alias_exception import AliasException
from ._duplicate_hook_error import DuplicateHookError
from ._type_cast_exception import TypeCastException
from ._hash_mismatch import HashMismatch
from ._cast_mismatch import CastMismatch
from ._flex_mismatch import FlexMismatch
from ._kee_num_type_exception import KeeNumTypeException
from ._empty_kee_num_error import EmptyKeeNumError
from ._duplicate_kee_num import DuplicateKeeNum
from ._unpack_exception import UnpackException
from ._dispatch_exception import DispatchException
from ._missing_variable import MissingVariable
from ._variable_not_none import VariableNotNone
from ._questionable_syntax import QuestionableSyntax
from ._read_only_error import ReadOnlyError
from ._reserved_name import ReservedName
from ._hook_exception import HookException
from ._write_once_error import WriteOnceError
from ._subclass_exception import SubclassException
from ._protected_error import ProtectedError
from ._type_exception import TypeException
from ._path_syntax_exception import PathSyntaxException
from ._illegal_instantiation import IllegalInstantiation
from ._del_exception import DelException

__all__ = [
    'attributeErrorFactory',
    'AccessError',
    'MetaclassException',
    'AliasException',
    'HashMismatch',
    'CastMismatch',
    'FlexMismatch',
    'EmptyKeeNumError',
    'KeeNumTypeException',
    'DuplicateKeeNum',
    'DuplicateHookError',
    'TypeCastException',
    'UnpackException',
    'DispatchException',
    'MissingVariable',
    'VariableNotNone',
    'QuestionableSyntax',
    'ReadOnlyError',
    'ReservedName',
    'HookException',
    'WriteOnceError',
    'SubclassException',
    'ProtectedError',
    'TypeException',
    'PathSyntaxException',
    'IllegalInstantiation',
    'ZerotonCaseException',
    'DelException'
]
