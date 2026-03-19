"""
The 'worktoy.markwork' facilitates systematic creation of documentation in
Markdown.

Please note that Markdown is *not* fit for the purpose of writing
documentation (or any other purpose). It is an impediment to creation of
documentation, it lacks consistency across renderers and requires tooling
such as provided here.

The tooling provided here is targeted towards GitHub, and is undefined for
any other renderer. It is an ambition of the 'worktoy' library to provide
a clean 'LateX'-like replacement for the purpose of writing documentation
that renders consistently across both platforms *and* formats. This means
the same documentation has a consistent presentation in 'pdf' file,
on a website and in a terminal presentation such as a 'man' page.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._header_num import HeaderNum
from ._style import Style
from ._sub_section_style import SubSectionStyle
from ._section_style import SectionStyle
from ._chapter_style import ChapterStyle
from ._title_style import TitleStyle

from ._inline_base import InlineBase
from ._badge import Badge
from ._inline_text import InlineText
from ._inline_lorem import InlineLorem
from ._inline_link import InlineLink

from ._inline_hook import InlineHook
from ._block_hook import BlockHook
from ._block_space import BlockSpace
from ._meta_block import MetaBlock

from ._block import Block
from ._code_block import CodeBlock
from ._source_block import SourceBlock

from ._paragraph_block import ParagraphBlock
from ._sub_section import SubSection
from ._section import Section
from ._chapter import Chapter
from ._index import Index

__all__ = [
  'HeaderNum',
  'Style',
  'SubSectionStyle',
  'SectionStyle',
  'ChapterStyle',
  'TitleStyle',
  'InlineBase',
  'Badge',
  'InlineText',
  'InlineLorem',
  'InlineLink',
  'InlineHook',
  'BlockHook',
  'BlockSpace',
  'MetaBlock',
  'Block',
  'CodeBlock',
  'SourceBlock',
  'ParagraphBlock',
  'SubSection',
  'Section',
  'Chapter',
  'Index',
  ]
