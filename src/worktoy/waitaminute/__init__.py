"""WorkToy - WaitAMinute
Decorator-based custom exception"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._meta_xcept import MetaXcept
from ._missing_argument_exception import MissingArgumentException
from ._type_support_error import TypeSupportError
from ._meta_type_support_error import MetaTypeSupportError
from ._unavailable_name import UnavailableNameException
from ._unsupported_subclass_exception import UnsupportedSubclassException
from ._recursive_create_get_error import RecursiveCreateGetError
from ._protected_attribute_error import ProtectedAttributeError
from ._read_only_exception import ReadOnlyException
from ._unexpected_state_exception import UnexpectedStateError
