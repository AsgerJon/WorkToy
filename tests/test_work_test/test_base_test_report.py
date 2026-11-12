"""
TestBaseTestReport tests how 'BaseTest' from 'worktoy.work_test' sees to
the report of the failed 'subTest' blocks of a test.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import unittest

from worktoy.mcls import BaseMeta
from worktoy.work_test import BaseTest
from . import WorkTestTest


class TestBaseTestReport(WorkTestTest):
  """
  A failed 'subTest' block is recorded, and the test must fail with the
  records afterwards, whatever the test class does. '__class_init__' of
  'BaseTest' gives every test class test methods that report as they
  end, and a 'doCleanups' and a 'debug' that report, built around the
  ones the class would use otherwise, so the report needs no hand-on
  from a 'tearDown', a 'doCleanups', a 'debug' or a 'run' of the test
  class, and a test base may bring a metaclass of its own. The tests pin
  the metaclass and the two methods; the report beside a 'tearDown' that
  hands on, beside one that does not and without any; that it runs
  before the cleanups of the test and comes once; the report at the end
  of 'debug'; a test base with a metaclass of its own; a 'doCleanups' of
  the class that hands on, one that does not and one of a mixin listed
  first; a 'debug' of the class, handing on or not; which test methods
  are given the report; a test method called by hand; a 'run' of the
  class that does not hand on; a 'doCleanups' put on the class after it
  is created; a block failing inside a cleanup; that a skip and an
  expected failure stay what they are; and a test base with a
  '__class_init__' of its own that hands on.
  """

  @staticmethod
  def _run(case: type) -> unittest.TestResult:
    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(case).run(result)
    return result

  def assertReported(self, result: unittest.TestResult) -> None:
    """One failure naming the failed block, and no error."""
    self.assertEqual(len(result.failures), 1)
    self.assertEqual(result.errors, [])
    self.assertIn('FAIL [n=1]: 1 != 2', result.failures[0][1])

  def test_shape(self) -> None:
    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the class is built for its shape alone."""

    class Own(BaseTest):
      def doCleanups(self) -> None:
        """Never runs: the class is built for its shape alone."""

      def debug(self) -> None:
        """Never runs either."""

    self.assertIs(type(BaseTest), BaseMeta)
    self.assertNotIn('tearDown', vars(BaseTest))
    for name in ('doCleanups', 'debug'):
      with self.subTest(name=name):
        given = vars(BaseTest)[name]
        self.assertEqual(given.__name__, name)
        self.assertTrue(given.__reports__)
        self.assertIsNot(given, vars(unittest.TestCase)[name])
        #  A class that writes none uses the one of its base as it is.
        self.assertNotIn(name, vars(Case))
        #  A class that writes one is given one built around its own.
        built = vars(Own)[name]
        self.assertEqual(built.__name__, name)
        self.assertTrue(built.__reports__)
        self.assertIsNot(built, given)

  def test_report_beside_a_tear_down_that_does_not_hand_on(self) -> None:
    log = []

    class Case(BaseTest):
      def tearDown(self) -> None:
        log.append('tearDown ran')

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    result = self._run(Case)
    self.assertEqual(result.testsRun, 1)
    self.assertReported(result)
    self.assertEqual(log, ['tearDown ran'])

  def test_report_beside_a_tear_down_that_hands_on(self) -> None:
    log = []

    class Case(BaseTest):
      def tearDown(self) -> None:
        BaseTest.tearDown(self)
        log.append('tearDown ran to its end')

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    self.assertReported(self._run(Case))
    self.assertEqual(log, ['tearDown ran to its end'])

  def test_no_report_when_nothing_failed(self) -> None:
    class Case(BaseTest):
      def tearDown(self) -> None:
        """Hands nothing on, and nothing is lost."""

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 1)

      def test_plain(self) -> None:
        self.assertEqual(1, 1)

    result = self._run(Case)
    self.assertEqual(result.testsRun, 2)
    self.assertTrue(result.wasSuccessful())

  def test_report_runs_before_the_cleanups_of_the_test(self) -> None:
    seen = []

    class Case(BaseTest):
      def setUp(self) -> None:
        self.addCleanup(self._look)

      def _look(self) -> None:
        seen.append('__sub_test__' in vars(self))

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)
        seen.append('__sub_test__' in vars(self))

    self.assertReported(self._run(Case))
    #  The records are there after the test and gone, reported, by the
    #  time the cleanup of the test runs.
    self.assertEqual(seen, [True, False])

  def test_failure_reported_once(self) -> None:
    class Case(BaseTest):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)
        self.doCleanups()

    result = self._run(Case)
    self.assertEqual(result.testsRun, 1)
    self.assertReported(result)

  def test_debug_reports(self) -> None:
    class Case(BaseTest):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

      def test_fine(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 1)

      def test_raises(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)
        raise KeyError('first out')

    with self.assertRaises(AssertionError) as context:
      Case('test_block').debug()
    self.assertIn('FAIL [n=1]: 1 != 2', str(context.exception))
    self.assertIsNone(Case('test_fine').debug())
    #  What the test itself raises flies out first, as 'debug' is for.
    with self.assertRaises(KeyError) as context:
      Case('test_raises').debug()
    self.assertEqual(context.exception.args, ('first out',))

  def test_metaclass_of_the_test_base(self) -> None:
    class OwnMeta(BaseMeta):
      """A metaclass of the test base's own, as a project may bring."""

    class OwnBase(BaseTest, metaclass=OwnMeta):
      """A test base built by it."""

    class Case(OwnBase):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

      def test_fine(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 1)

    self.assertIs(type(Case), OwnMeta)
    result = self._run(Case)
    self.assertEqual(result.testsRun, 2)
    self.assertReported(result)

  def test_do_cleanups_of_the_class_that_hands_on(self) -> None:
    log = []

    class Named(BaseTest):
      def doCleanups(self) -> bool:
        log.append('doCleanups of the class')
        return BaseTest.doCleanups(self)

      def test_block(self) -> None:
        self.addCleanup(log.append, 'a cleanup of the test')
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    class Super(BaseTest):
      def doCleanups(self) -> bool:
        log.append('doCleanups of the class')
        return super().doCleanups()

      def test_block(self) -> None:
        self.addCleanup(log.append, 'a cleanup of the test')
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    for case in (Named, Super):
      with self.subTest(case=case.__name__):
        log.clear()
        self.assertReported(self._run(case))
        self.assertEqual(log, ['doCleanups of the class',
                               'a cleanup of the test'])

  def test_do_cleanups_of_the_class_that_does_not_hand_on(self) -> None:
    log = []

    class Case(BaseTest):
      def doCleanups(self) -> bool:
        log.append('doCleanups of the class')
        return True

      def test_block(self) -> None:
        self.addCleanup(log.append, 'a cleanup of the test')
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    self.assertReported(self._run(Case))
    #  What 'unittest' promises of a cleanup holds as well: it runs.
    self.assertEqual(log, ['doCleanups of the class',
                           'a cleanup of the test'])

  def test_do_cleanups_of_a_mixin_listed_first(self) -> None:
    class Ahead:
      def doCleanups(self) -> bool:
        return True

    class Case(Ahead, BaseTest):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    self.assertTrue(vars(Case)['doCleanups'].__reports__)
    self.assertReported(self._run(Case))

  def test_debug_of_the_class(self) -> None:
    log = []

    class HandsOn(BaseTest):
      def debug(self) -> None:
        log.append('debug of the class')
        BaseTest.debug(self)

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    class Alone(BaseTest):
      def debug(self) -> None:
        log.append('debug of the class')
        self.test_block()

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    for case in (HandsOn, Alone):
      with self.subTest(case=case.__name__):
        with self.assertRaises(AssertionError) as context:
          case('test_block').debug()
        self.assertIn('FAIL [n=1]: 1 != 2', str(context.exception))
    self.assertEqual(log, ['debug of the class', 'debug of the class'])

  def test_test_methods_are_given_the_report(self) -> None:
    class Mixed:
      def test_mixed(self) -> None:
        """A test method of a plain mixin."""

    class Case(Mixed, BaseTest):
      testData = (1, 2)

      def test_own(self) -> None:
        """The docstring of the test."""

      async def test_later(self) -> None:
        """Never runs: a coroutine function is left as it is."""

      @staticmethod
      def test_static() -> None:
        """Never runs: it is no plain function of the class."""

      def helper(self) -> None:
        """Never runs: it is no test method."""

    class Sub(Case):
      """Writes no test method of its own."""

    own = vars(Case)['test_own']
    self.assertTrue(own.__reports__)
    self.assertEqual(own.__name__, 'test_own')
    self.assertEqual(own.__doc__, 'The docstring of the test.')
    mixed = vars(Case)['test_mixed']
    self.assertTrue(mixed.__reports__)
    self.assertIs(mixed.__wrapped__, vars(Mixed)['test_mixed'])
    self.assertFalse(hasattr(vars(Case)['test_later'], '__reports__'))
    self.assertIsInstance(vars(Case)['test_static'], staticmethod)
    self.assertEqual(Case.testData, (1, 2))
    self.assertFalse(hasattr(vars(Case)['helper'], '__reports__'))
    #  A class that inherits a test method uses it as it is.
    self.assertNotIn('test_own', vars(Sub))
    self.assertNotIn('test_mixed', vars(Sub))

  def test_test_method_called_by_hand(self) -> None:
    class Case(BaseTest):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

      def test_fine(self) -> int:
        with self.subTest(n=1):
          self.assertEqual(1, 1)
        return 7

    with self.assertRaises(AssertionError) as context:
      Case('test_block').test_block()
    self.assertIn('FAIL [n=1]: 1 != 2', str(context.exception))
    self.assertEqual(Case('test_fine').test_fine(), 7)

  def test_run_of_the_class_that_does_not_hand_on(self) -> None:
    class Case(BaseTest):
      def run(self, result: object = None) -> object:
        getattr(self, self._testMethodName)()
        return result

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

      def test_fine(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 1)

    with self.assertRaises(AssertionError) as context:
      Case('test_block').run()
    self.assertIn('FAIL [n=1]: 1 != 2', str(context.exception))
    self.assertEqual(Case('test_fine').run('as given'), 'as given')

  def test_do_cleanups_rebound_after_the_class(self) -> None:
    class Case(BaseTest):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    Case.doCleanups = lambda self: True
    self.assertReported(self._run(Case))

  def test_block_of_a_cleanup(self) -> None:
    class Case(BaseTest):
      def test_fine(self) -> None:
        self.addCleanup(self._tidy)

      def _tidy(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    self.assertReported(self._run(Case))

  def test_skip_and_expected_failure_kept(self) -> None:
    class Case(BaseTest):
      @unittest.skip('not today')
      def test_skipped(self) -> None:
        """Never runs: it is skipped."""

      @unittest.expectedFailure
      def test_expected(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    result = self._run(Case)
    self.assertEqual(result.testsRun, 2)
    self.assertEqual([why for _, why in result.skipped], ['not today'])
    self.assertEqual(len(result.expectedFailures), 1)
    self.assertEqual(result.failures, [])
    self.assertEqual(result.errors, [])

  def test_class_init_of_the_test_base_that_hands_on(self) -> None:
    seen = []

    class OwnBase(BaseTest):
      @classmethod
      def __class_init__(cls, name: str, bases: tuple, space, **kw) -> None:
        seen.append(name)
        super().__class_init__(name, bases, space, **kw)

    class Case(OwnBase):
      def doCleanups(self) -> bool:
        return True

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

    self.assertEqual(seen, ['OwnBase', 'Case'])
    self.assertReported(self._run(Case))
