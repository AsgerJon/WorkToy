"""
LoremTest is the local base of the 'tests.test_lorem_ipsum' folder.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import random

from worktoy.work_test import BaseTest


class LoremTest(BaseTest):
  """
  The tests of one folder want one base of their own, so that what the
  folder shares has one home. 'LoremTest' is that base for the tests of
  'worktoy.lorem_ipsum': it seeds the samplers and the 'random' module
  the generators draw from, so every draw and every text repeats from
  run to run.

  Implementation
  --------------

  'setUp' seeds the six samplers of 'BaseTest' and 'random' with one
  fixed seed.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __sampler_seed__: int = 2718

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    self.seedSamplers(self.__sampler_seed__)
    random.seed(self.__sampler_seed__)
