"""
WorkTestTest is the local base of the 'tests.test_work_test' folder.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

  from worktoy.waitaminute import TypeException


class WorkTestTest(BaseTest):
  """
  The tests of one folder want one base of their own, so that what the
  folder shares has one home. 'WorkTestTest' is that base for the tests
  of 'worktoy.work_test': it seeds the samplers, so every draw repeats
  from run to run, and it holds the one assertion the folder makes at
  nearly every refusal, that a 'TypeException' names the setting, the
  value and the type expected.

  Implementation
  --------------

  'setUp' seeds the six samplers of 'BaseTest' with one fixed seed.
  'assertTypeRefused' asserts the four slots of a 'TypeException' and
  the two names its text carries.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __sampler_seed__: int = 1414

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    self.seedSamplers(self.__sampler_seed__)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def assertTypeRefused(self, exception: TypeException, name: str,
                        value: Any, expected: type) -> None:
    """The exception names the setting, the value and the expected type."""
    self.assertEqual(exception.varName, name)
    self.assertEqual(exception.actualObject, value)
    self.assertIs(exception.actualType, type(value))
    self.assertEqual(exception.expectedTypes, (expected,))
    self.assertIn("'%s' to be an instance of '%s'"
                  % (name, expected.__name__), str(exception))
