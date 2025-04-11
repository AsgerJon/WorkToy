"""The 'worktoy.static' module provides low level parsing and casting
utilities. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._this import THIS
from ._deleted import DELETED
from ._type_sig import TypeSig
from . import casting

from ._dispatch import Dispatch
from ._overload import overload
