"""WorkToy - WorkSide - Widgets - FontFamilies
Provides a list of supported font families"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

_families = """Arial,
               Times New Roman,
               Courier New,
               Verdana,
               Cambria,
               Tahoma,
               Calibri,
               Comic Sans MS,
               Helvetica,
               Geneva,
               Lucida Grande,
               DejaVu Sans,
               DejaVu Serif,
               DejaVu Sans Mono,
               Liberation Sans,
               Liberation Serif,
               Liberation Mono,
               Ubuntu,
               Cantarell,
               Droid Sans,
               Droid Serif,
               Roboto,
               Roboto Condensed,
               Roboto Mono,
               Noto Sans,
               Noto Serif,
               Noto Sans Mono,
               Source Sans Pro,
               Source Serif Pro,
               Source Code Pro,
               Modern No. 20"""

data = _families.replace('\n', '').split(',')
FAMILIES = [item.strip() for item in data]
