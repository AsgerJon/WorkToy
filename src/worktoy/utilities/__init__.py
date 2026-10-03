"""Leaf-level utilities used across 'worktoy'.

This package collects small, standalone helpers with no
'worktoy' dependencies: text formatting ('textFmt',
'stringList', 'joinWords', 'wordWrap'), iterable handling
('unpack', 'maybe'), slicing ('sliceLen', 'ValidSlice'),
type/MRO helpers ('typeCast', 'castRule', 'resolveMRO'), descriptor
support ('QuickDesc'), filesystem ('Directory'), exception
inspection ('ExceptionInfo'), the refusal of the pickle protocol
('NoPickle'), the 'combinatorics' subpackage, and a handful of
orphans ('argsCount', 'bipartiteMatching', 'replaceFlex',
'ClassBodyTemplate')."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

#  Requiring no local imports
from ._no_pickle import NoPickle
from ._class_body_template import ClassBodyTemplate
from ._args_count import argsCount
from ._bipartite_matching import bipartiteMatching
from ._unpack import unpack
from ._slice_len import sliceLen
from ._maybe import maybe
from ._text_fmt import textFmt
from ._string_list import stringList
#  Requiring 'NoPickle'
from ._directory import Directory
#  Requiring 'unpack'
from ._join_words import joinWords
#  Requiring no local imports
from ._word_wrap import wordWrap
#  Requiring 'maybe'
from ._replace_flex import replaceFlex
#  Requiring 'textFmt' and 'NoPickle'
from ._quick_desc import QuickDesc
#  Requiring 'textFmt'
from ._valid_slice import ValidSlice
#  Requiring 'textFmt', 'QuickDesc' and 'NoPickle'
from ._exception_info import ExceptionInfo
#  Requiring 'joinWords' and 'textFmt'
from ._resolve_mro import resolveMRO
#  Requiring 'ValidSlice'
from ._type_cast import typeCast, castRule
#  Requiring 'QuickDesc', 'textFmt' and 'NoPickle'
from . import combinatorics

__all__ = [
  'NoPickle',
  'ClassBodyTemplate',
  'argsCount',
  'bipartiteMatching',
  'unpack',
  'sliceLen',
  'maybe',
  'textFmt',
  'QuickDesc',
  'stringList',
  'Directory',
  'joinWords',
  'wordWrap',
  'replaceFlex',
  'typeCast',
  'castRule',
  'ValidSlice',
  'ExceptionInfo',
  'resolveMRO',
  'combinatorics',
]
