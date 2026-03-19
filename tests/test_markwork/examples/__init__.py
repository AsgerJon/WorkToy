"""
The 'tests.test_markwork.examples' package provides examples used by the
tests in the 'tests.test_markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._install_block import InstallBlock
from ._readme_example import ReadmeExample
from ._lorem_sub_section import LoremSubSection
from ._lorem_section import LoremSection
from ._lorem_chapter import LoremChapter
from ._lorem_chapter_child import LoremChapterChild

__all__ = [
  'InstallBlock',
  'ReadmeExample',
  'LoremSubSection',
  'LoremSection',
  'LoremChapter',
  'LoremChapterChild',
  ]
