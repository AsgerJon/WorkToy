"""
_BLACK_LISTED_TYPES lists types that are explicitly blacklisted from
appearing in the class body of an EZData class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Alias
from worktoy.dispatch import Dispatcher

_BLACK_LISTED_TYPES = (Alias, Dispatcher)
