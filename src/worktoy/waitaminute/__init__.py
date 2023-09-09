"""WorkToy - WaitAMinute
Decorator-based custom exception"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._except_space import ExceptSpace
from ._meta_xcept import MetaXcept
from ._type_support_error import TypeSupportError
from ._unexpected_state_error import UnexpectedStateError
from ._recursive_create_get_error import RecursiveCreateGetError
from ._value_exists_error import ValueExistsError
from ._meta_type_support_error import MetaTypeSupportError
from ._dispatcher_exception import DispatcherException
from ._unavailable_name import UnavailableNameException
from ._unsupported_subclass_exception import UnsupportedSubclassException
