"""
TestMeta is a metaclass a test base may choose. Under it, a class body
that binds 'doCleanups' or 'debug' is refused at that line.
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
  'BaseTest' reports the failed 'subTest' blocks of a test from three
  places: each test method as it ends, 'doCleanups' after the cleanups
  of the test, and 'debug' at its end. It gives every test class a
  'doCleanups' and a 'debug' that report, built around the ones the
  class writes itself when it writes any, so a class that writes its
  own loses no report. A test base may still prefer that the bodies of
  its test classes leave the two names alone, and that a body binding
  one is refused at that line. TestMeta is the metaclass such a base
  chooses. 'BaseTest' itself is not built by it, so that a test base
  may bring any metaclass based on 'BaseMeta'.

    class StrictTest(BaseTest, metaclass=TestMeta):
      pass

    class TestDice(StrictTest):

      def doCleanups(self) -> None:  # refused here, with 'ReservedName'
        self.table.close()

  Implementation
  --------------

  '__prepare__' returns a 'TestSpace' in which 'doCleanups' and 'debug'
  are bound already, to the functions '_doCleanupsFactory' and
  '_debugFactory' make, and which refuses a class body binding either
  name. The 'doCleanups' placed registers 'BaseTest._reportSubTests'
  with 'addCleanup' and calls 'TestCase.doCleanups': an exception
  raised in 'doCleanups' itself would leave 'TestCase.run', where one
  raised by a registered cleanup is collected as a failure of the test.
  Registered last, the report runs first, before the cleanups of the
  test. The 'debug' placed calls 'TestCase.debug' and then the report,
  whose exception leaves 'debug' as any exception of the test does.
  'BaseTest.__class_init__' builds its own 'doCleanups' and 'debug'
  around the two, as around any a class body binds, so those are what
  the class holds in its '__dict__', and the report runs once more
  after the cleanups of the test, for a block that failed inside one.
  Only the class body is refused: a name assigned on the class after
  the class statement is not.
  """

  @staticmethod
  def _doCleanupsFactory() -> Callable:
    """
    Every class 'TestMeta' builds must find a 'doCleanups' of the
    library in its namespace before its body runs.

    Implementation
    --------------

    A new function is made at each call, so each class holds one of its
    own. It registers 'BaseTest._reportSubTests' as a cleanup, the last,
    and returns what 'TestCase.doCleanups' returns.

    Returns
    -------

    Callable
      Called as '(self)': the 'doCleanups' of one test class.
    """

    def doCleanups(self: Any) -> bool:
      self.addCleanup(self._reportSubTests)
      return TestCase.doCleanups(self)

    return doCleanups

  @staticmethod
  def _debugFactory() -> Callable:
    """
    Every class 'TestMeta' builds must find a 'debug' of the library in
    its namespace before its body runs, as it finds a 'doCleanups'.

    Implementation
    --------------

    A new function is made at each call, so each class holds one of its
    own. It calls 'TestCase.debug', which collects no errors and runs no
    'doCleanups', and then 'BaseTest._reportSubTests'.

    Returns
    -------

    Callable
      Called as '(self)': the 'debug' of one test class.
    """

    def debug(self: Any) -> None:
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
