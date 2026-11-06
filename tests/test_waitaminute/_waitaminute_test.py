"""
WaitaminuteTest is the local base of the 'tests.test_waitaminute' folder.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest


class WaitaminuteTest(BaseTest):
  """
  The tests of one folder want one base of their own, so that what the
  folder shares has one home. 'WaitaminuteTest' is that base for the
  tests of 'worktoy.waitaminute': it seeds the samplers, so the names
  the tests build at random repeat from run to run.

  Implementation
  --------------

  'setUp' seeds the six samplers of 'BaseTest' with one fixed seed.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __sampler_seed__: int = 1618

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    self.seedSamplers(self.__sampler_seed__)
