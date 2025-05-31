"""
The '_reservedNames' 'list' contains the names that classes derived from
Zeroton may not use. These names are disallowed to ensure the intended
functionality of Zeroton classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

_reservedNames = [
    '__new__',
    '__init__',
    '__call__',
]
