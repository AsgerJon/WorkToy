"""
UtilitiesTest is the local base of the 'tests.test_utilities' folder.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest


class UtilitiesTest(BaseTest):
  """
  The tests of one folder want one base of their own, so that what the
  folder shares, a seed for the samplers at the moment, has one home
  and the folder can grow a helper without touching every file.
  'UtilitiesTest' is that base for the tests of 'worktoy.utilities'.

  Implementation
  --------------

  'setUp' seeds the six samplers of 'BaseTest' with one fixed seed, so
  every draw of a test in the folder repeats from run to run.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __sampler_seed__: int = 1234

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    self.seedSamplers(self.__sampler_seed__)
