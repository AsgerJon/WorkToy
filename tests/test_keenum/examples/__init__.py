"""
The 'tests.test_keenum.examples' package provides example subclasses of
the KeeFlags class for testing and demonstration purposes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._rgb import RGB
from ._flags_example import FlagsExample
from ._subclass_example import SubclassExample
from ._prime_valued import PrimeValued
from ._file_access import FileAccess
from ._keyboard_modifier import KeyboardModifier
from ._mouse_button import MouseButton
from ._rgb_num import RootRGB, MoreRGB, EvenMoreRGB, RGBNum
from ._brush import Brush

__all__ = [
    'RGB',
    'FlagsExample',
    'SubclassExample',
    'PrimeValued',
    'FileAccess',
    'KeyboardModifier',
    'MouseButton',
    'RootRGB',
    'MoreRGB',
    'EvenMoreRGB',
    'RGBNum',
    'Brush',
]
