"""
The 'worktoy.work_test' package provides the testing support shared across
the worktoy suite. 'BaseTest' is the 'unittest.TestCase' subclass every
test class is based on, wiring in the random-data samplers and the
'SubTest' accumulator. 'TestMeta' is its metaclass and 'TestSpace' the
namespace of a test class; together they see to it that the failed
blocks of a test are reported whatever the test class does in
'tearDown'. 'ComplexMixin' and 'ComplexTest' are a worked
example: a complex-number mixin and the parametrized test bank that runs
one dunder suite against any number of its implementations.

- samplers
- SubTest
- TestSpace
- TestMeta
- BaseTest
- ComplexMixin
- ComplexTest
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import samplers
from ._sub_test import SubTest
from ._test_space import TestSpace
from ._test_meta import TestMeta
from ._base_test import BaseTest
from ._complex_mixin import ComplexMixin
from ._complex_test import ComplexTest

__all__ = [
  'samplers',
  'SubTest',
  'TestSpace',
  'TestMeta',
  'BaseTest',
  'ComplexMixin',
  'ComplexTest',
]
