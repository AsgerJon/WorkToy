"""
The 'tests.test_keenum.examples' package provides example subclasses of
the KeeFlags class for testing and demonstration purposes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._h_alignum import HAlignum
from ._v_alignum import VAlignum
from ._rgb import RGB
from ._color_num import ColorNum
from ._pen import Pen
from ._flags_example import FlagsExample
from ._subclass_example import SubclassExample
from ._prime_valued import PrimeValued
from ._file_access import FileAccess
from ._keyboard_modifier import KeyboardModifier
from ._mouse_button import MouseButton
from ._rgb_num import RootRGB, MoreRGB, EvenMoreRGB, RGBNum
from ._week_day import WeekDay
from ._dag import _MetaDag, Dag
from ._ugedag import Ugedag
from ._compass import Compass
from ._month import Month
from ._dato import Dato
from ._brush import Brush

__all__ = [
  'HAlignum',
  'VAlignum',
  'RGB',
  'ColorNum',
  'Pen',
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
  'WeekDay',
  '_MetaDag',
  'Dag',
  'Ugedag',
  'Compass',
  'Month',
  'Dato',
  'Brush',
  ]
