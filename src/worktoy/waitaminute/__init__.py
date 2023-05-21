"""Documentation: waitaminute
This package contains more precise exceptions than those found builtin.
This is motivated because the same exception for example TypeError is used
in too many different situations."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._readonlyerror import ReadOnlyError
from ._exceptioncore import ExceptionCore
from ._instantiationerror import InstantiationError
from ._proceduralerror import ProceduralError
