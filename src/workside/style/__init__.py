"""WorkToy - WorkSide - Style
This module provides style functions"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from ._rgb import RGB
from ._rgb import RGBField
from ._alignment_sym import AlignmentSym
from ._font_family_names import FAMILIES
from ._font_weight_names import WEIGHTS

from ._font_weight_sym import FontWeight
from ._font_weight_field import FontWeightField
from ._font_family_sym import FontFamily
from ._font_family_field import FontFamilyField
from ._font_size import FontSize
from ._font_size_field import FontSizeField

from ._pen_sym import PenSym
from ._pen_sym_field import PenSymField
from ._brush_sym import BrushSym
from ._brush_sym_field import BrushSymFill

from ._line_style import Line, lineBase
from ._font_style import Font, fontBase
from ._fill_style import Fill, fillBase
from ._style import Style, styleBase
