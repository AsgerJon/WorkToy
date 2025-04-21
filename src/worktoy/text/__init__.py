"""The 'worktoy.text' package contains modules for working with text data."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._mono_space import monoSpace
from ._join_words import joinWords
from ._type_msg import typeMsg
from ._string_list import stringList
from ._word_wrap import wordWrap
from ._func_report import funcReport

__all__ = [
    'monoSpace',
    'typeMsg',
    'joinWords',
    'stringList',
    'wordWrap',
    'funcReport',
]
