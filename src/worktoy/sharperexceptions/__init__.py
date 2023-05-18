"""Documentation: sharperexceptions
This package contains more precise exceptions than those found builtin.
This is motivated because the same exception for example TypeError is used
in too many different situations."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._argumenterror import ArgumentError
from ._parsingerror import ParsingError
from ._readonlyerror import ReadOnlyError
from ._testexception import TestException
