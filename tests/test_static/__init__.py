"""The 'test_static' module tests the 'worktoy.static' module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._number import Number
from ._complex_number import ComplexNumber
from ._hist_name_space import HistNameSpace
from ._hist_metaclass import HistMetaclass

__all__ = [
    'ComplexNumber',
    'Number',
    'HistNameSpace',
    'HistMetaclass'
]
