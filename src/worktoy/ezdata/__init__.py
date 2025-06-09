"""
The 'worktoy.ezdata' package provides the EZData dataclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen

from ._data_field import DataField
from ._ez_hook import EZHook
from ._ez_space import EZSpace
from ._ez_meta import EZMeta
from ._ez_data import EZData

__all__ = [
    'DataField',
    'EZHook',
    'EZSpace',
    'EZMeta',
    'EZData',
]
