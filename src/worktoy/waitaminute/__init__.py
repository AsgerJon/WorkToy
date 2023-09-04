"""WorkToy - WaitAMinute
Decorator-based custom exception"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._except_space import ExceptSpace
from ._meta_xcept import MetaXcept
from ._chill_out_exception import ChillOutException
from ._argument_error import ArgumentError
from ._disabled_method_error import DisabledFunctionError
from ._type_support_error import TypeSupportError
from ._protected_field_error import ProtectedFieldError
from ._secret_field_error import SecretFieldError
from ._readonly_error import ReadOnlyError
from ._unexpected_state_error import UnexpectedStateError
from ._recursive_create_get_error import RecursiveCreateGetError
from ._value_exists_error import ValueExistsError
from ._meta_type_support_error import MetaTypeSupportError
from ._type_signature_exception import TypeSignatureException
from ._dispatcher_exception import DispatcherException
from ._missing_annotations_error import MissingAnnotationsError
from ._symbolic_conversion_error import SymbolicConversionError
from ._spacing_point_error import SpacingPointError
from ._type_guard_error import TypeGuardError
