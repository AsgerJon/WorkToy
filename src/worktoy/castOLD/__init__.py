"""The 'worktoy.static' module provides low level parsing and casting
utilities. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._maybe import maybe
from ._maybe_type import maybeType
from ._zero_this import THIS, thisFilterFactory
from ._complex_cast import ComplexCastException, complexCast
from ._float_cast import FloatCastException, floatCast
from ._int_cast import IntCastException, intCast
from ._num_cast import numCast
from ._type_cast import typeCast
from ._type_sig import TypeSig
from ._overload_entry import OverloadEntry, overload
from ._dispatch import Dispatch
