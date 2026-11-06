"""
The 'tests.test_lorem_ipsum' package tests 'worktoy.lorem_ipsum': the
word lists, the bounded distributions 'StochasticVariable',
'GaussianLengths' and 'StochasticWord', and the generators
'BaseGenerator', 'Clause', 'Sentence' and 'Paragraph'. Every test class
is based on 'LoremTest', the local base of the folder, and the fixtures
the tests share are small classes of their own.

- LoremTest

Private, importable but not intended for public use:

- Narrow
- NarrowClause
- Hailed
- Noted
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._lorem_test import LoremTest
from ._narrow import Narrow
from ._narrow_clause import NarrowClause
from ._hailed import Hailed
from ._noted import Noted

__all__ = [
  'LoremTest',
]
