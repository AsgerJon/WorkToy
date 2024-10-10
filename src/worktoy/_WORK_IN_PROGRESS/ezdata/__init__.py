"""The 'worktoy.ezdata' class provides the EZData class!"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._ezption import IllegalMethodException, IllegalInitException
from ._ezption import NoDefaultError, AmbiguousDefaultError
from ._ezption import DefaultTypeMismatchError
from ._ez_space import EZSpace
from ._ez_meta import EZMeta
from ._ez_data import EZData
