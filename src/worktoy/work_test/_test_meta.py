"""
TestMeta is the metaclass of 'BaseTest'. It keeps 'doCleanups' and
'debug', from which the failed 'subTest' blocks are reported, out of the
reach of a test class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import TestCase

from . import TestSpace
from ..mcls import BaseMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable


class TestMeta(BaseMeta):
  """
  A failed 'subTest' block of a 'BaseTest' is swallowed and recorded, so
  something must run after every test and fail it with the records, or
  a failed block passes for a success. 'unittest' offers 'tearDown' for
  what runs after a test, but a test class overrides 'tearDown' as a
  matter of course, and the override need not hand on. 'unittest' also
  runs 'doCleanups' after every test, whatever the test class did with
  'tearDown', and a test class has no reason to touch it; a test run
  with 'debug', which collects no errors, skips 'doCleanups' and ends in
  'debug' itself. TestMeta is the metaclass of 'BaseTest': it puts the
  library's own 'doCleanups' and 'debug' into the namespace of every
  class it builds, before the class body runs, and the namespace
  refuses a class body that binds either name.

    class TestDice(BaseTest):

      def tearDown(self) -> None:
        self.table.close()  # the report needs no hand-on

  Implementation
  --------------

  '__prepare__' returns a 'TestSpace' in which 'doCleanups' and 'debug'
  are bound already, to the functions '_doCleanupsFactory' and
  '_debugFactory' make, so every class holds the two methods in its own
  '__dict__' and no base ahead of it in the resolution order is found
  first. 'doCleanups' registers 'BaseTest._reportSubTests' with
  'addCleanup' and calls 'TestCase.doCleanups': an exception raised in
  'doCleanups' itself would leave 'TestCase.run', where one raised by a
  registered cleanup is collected as a failure of the test. Registered
  last, the report runs first, before the cleanups of the test. 'debug'
  calls 'TestCase.debug' and then the report, whose exception leaves
  'debug' as any exception of the test does.
  """

  @staticmethod
  def _doCleanupsFactory() -> Callable:
    """
    The '_doCleanupsFactory' method makes the 'doCleanups' of one test
    class.
    """

    def doCleanups(self: Any) -> bool:
      """
      Registers the report of the 'subTest' blocks as the last cleanup,
      then runs the cleanups as 'TestCase.doCleanups' does.
      """
      self.addCleanup(self._reportSubTests)
      return TestCase.doCleanups(self)

    return doCleanups

  @staticmethod
  def _debugFactory() -> Callable:
    """
    The '_debugFactory' method makes the 'debug' of one test class.
    """

    def debug(self: Any) -> None:
      """
      Runs the test as 'TestCase.debug' does, which collects no errors
      and runs no 'doCleanups', then the report of the 'subTest' blocks.
      """
      TestCase.debug(self)
      self._reportSubTests()

    return debug

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple, **kwargs) -> TestSpace:
    """
    The namespace of a test class holds the library's 'doCleanups' and
    'debug' before the first line of the class body runs.

    Parameters
    ----------

    name : str
      The name of the class.

    bases : tuple
      The bases of the class.

    Returns
    -------

    TestSpace
      The namespace, with 'doCleanups' and 'debug' bound.
    """
    space = TestSpace(mcls, name, bases, **kwargs)
    doCleanups = mcls._doCleanupsFactory()
    space.__setitem__('doCleanups', doCleanups, _root=True)
    debug = mcls._debugFactory()
    space.__setitem__('debug', debug, _root=True)
    return space
