"""
TestComplexBank runs the 'ComplexTest' bank of 'worktoy.work_test' for
real, against the implementation of this folder.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import ComplexTest
from . import WorkTestTest, SimpleComplex


class TestComplexBank(ComplexTest, WorkTestTest):
  """
  The bank used as a project uses it: listed before the local base with
  the implementation of this folder as its target, so its twenty-five
  tests run here as tests of the suite. The tests are the bank's own.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  targets = (SimpleComplex,)
