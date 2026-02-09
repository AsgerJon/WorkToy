"""
The 'worktoy.utilities' module provides small, standalone utilities used
across the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

#  Orphans not requiring local imports
from . import mathematics
from ._class_body_template import ClassBodyTemplate
from ._bipartite_matching import bipartiteMatching
from ._unpack import unpack
from ._perm import perm
from ._slice_len import sliceLen
from ._maybe import maybe
from ._text_fmt import textFmt
from ._string_list import stringList
from ._directory import Directory
from ._join_words import joinWords
from ._word_wrap import wordWrap

#  Requiring 'maybe'
from ._replace_flex import replaceFlex

#  Requiring 'textFmt'
from ._valid_slice import ValidSlice
from ._exception_info import ExceptionInfo

#  Requiring 'joinWords' and 'textFmt'
from ._resolve_mro import resolveMRO

#  Requiring 'ValidSlice'
from ._type_cast import typeCast

__all__ = [
  'mathematics',
  'ClassBodyTemplate',
  'bipartiteMatching',
  'unpack',
  'perm',
  'sliceLen',
  'maybe',
  'textFmt',
  'stringList',
  'Directory',
  'joinWords',
  'wordWrap',
  'replaceFlex',
  'typeCast',
  'ValidSlice',
  'ExceptionInfo',
  'resolveMRO',
]
