"""The waitAMinute module provides custom exceptions"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._exceptionparser import ExceptionParser
from ._dioerror import DIOError
from ._accessorerror import AccessorError
from ._invalidnamespaceerror import InvalidNameSpaceError
from ._readonlyerror import ReadOnlyError
from ._protectedpropertyerror import ProtectedPropertyError
from ._secretpropertyerror import SecretPropertyError
from ._testerror import TestError
