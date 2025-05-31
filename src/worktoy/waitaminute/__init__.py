"""The 'worktoy.waitaminute' module provides custom exception classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._attribute_error_factory import attributeErrorFactory
from ._attribute import _Attribute
from ._zeroton_case_exception import ZerotonCaseException
from ._bad_value import BadValue
from ._bad_set import BadSet
from ._bad_delete import BadDelete
from ._metaclass_exception import MetaclassException
from ._compound_exception import CompoundException
from ._alias_exception import AliasException
from ._abstract_exception import AbstractException
from ._hash_mismatch import HashMismatch
from ._cast_mismatch import CastMismatch
from ._flex_mismatch import FlexMismatch
from ._cast_exception import CastException
from ._instance_exception import InstanceException
from ._hash_error import HashError
from ._this_context_exception import THISContextException
from ._dispatch_exception import DispatchException
from ._parse_exception import ParseException
from ._resolve_exception import ResolveException
from ._missing_variable import MissingVariable
from ._variable_not_none import VariableNotNone
from ._questionable_syntax import QuestionableSyntax
from ._read_only_error import ReadOnlyError
from ._reserved_name import ReservedName
from ._hook_exception import HookException
from ._unrecognized_member import UnrecognizedMember
from ._write_once_error import WriteOnceError
from ._subclass_exception import SubclassException
from ._protected_error import ProtectedError
from ._type_exception import TypeException
from ._deleted_attribute_exception import DeletedAttributeException
from ._path_syntax_exception import PathSyntaxException
from ._illegal_instantiation_error import IllegalInstantiation
from ._illegal_name import IllegalName
from ._duplicate_seed_exception import DuplicateSeedException
from ._cascade_exception import CascadeException

__all__ = [
    'attributeErrorFactory',
    'BadValue',
    'BadSet',
    'BadDelete',
    'MetaclassException',
    'CompoundException',
    'AliasException',
    'HashMismatch',
    'CastMismatch',
    'FlexMismatch',
    'CastException',
    'InstanceException',
    'HashError',
    'IllegalName',
    'DispatchException',
    'ParseException',
    'ResolveException',
    'MissingVariable',
    'THISContextException',
    'VariableNotNone',
    'QuestionableSyntax',
    'ReadOnlyError',
    'ReservedName',
    'HookException',
    'UnrecognizedMember',
    'WriteOnceError',
    'SubclassException',
    'ProtectedError',
    'TypeException',
    'DeletedAttributeException',
    'PathSyntaxException',
    'IllegalInstantiation',
    'ZerotonCaseException',
    'DuplicateSeedException',
    'CascadeException'
]
