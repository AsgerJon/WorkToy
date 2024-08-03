"""The 'worktoy.yolo' package provides tools for testing functions and
running tests."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._lorem_ipsum import loremIpsum
from ._abstract_segment import AbstractSegment
from ._code_segment import CodeSegment
from ._text_segment import TextSegment
from ._lorem_segment import LoremSegment
from ._term_text import TermText

from ._yolo import yolo
from ._run_tests import runTests
