"""
TestTestMeta tests 'TestMeta' from 'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import unittest

from worktoy import work_test
from worktoy.mcls import BaseMeta, BaseSpace
from worktoy.waitaminute.meta import ReservedName
from worktoy.work_test import BaseTest
from . import WorkTestTest

#  'TestMeta' and 'TestSpace' are read through the package: bound in this
#  file under their own names, pytest would take them for test classes
#  and warn.


class TestTestMeta(WorkTestTest):
  """
  'TestMeta' builds 'BaseTest' and every test class based on it. It puts
  the library's own 'doCleanups' and 'debug' into the namespace of each
  class before the class body runs, and the namespace, a 'TestSpace',
  refuses the line of a class body that binds either name, so the report
  of failed 'subTest' blocks, which runs there, cannot be lost to an
  override. The tests pin the metaclass and the two methods in every
  class, the namespace, the refusal of each name at its line, the report
  beside a 'tearDown' that hands on, beside one that does not and
  without any, that a 'tearDown' runs to its end, that the report runs
  before the cleanups of the test, that a failure is reported once, and
  the report at the end of 'debug'.
  """

  @staticmethod
  def _run(case: type) -> unittest.TestResult:
    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(case).run(result)
    return result

  def test_shape(self) -> None:
    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the class is built for its namespace alone."""

    class Sub(Case):
      pass

    self.assertIsSubclass(work_test.TestMeta, BaseMeta)
    self.assertIsSubclass(work_test.TestSpace, BaseSpace)
    for cls in (BaseTest, Case, Sub):
      with self.subTest(cls=cls.__name__):
        self.assertIs(type(cls), work_test.TestMeta)
        for name in ('doCleanups', 'debug'):
          own = vars(cls)[name]
          self.assertEqual(own.__name__, name)
          self.assertIs(own.__code__, vars(BaseTest)[name].__code__)
    self.assertNotIn('tearDown', vars(BaseTest))
    #  The factories take no receiver, read through a class as well.
    self.assertEqual(BaseTest._doCleanupsFactory().__name__, 'doCleanups')
    self.assertEqual(BaseTest._debugFactory().__name__, 'debug')

  def test_namespace(self) -> None:
    space = work_test.TestMeta.__prepare__('Case', (BaseTest,))
    self.assertIs(type(space), work_test.TestSpace)

    def other(case: object) -> None:
      """Never runs: it is only bound."""

    for name in ('doCleanups', 'debug'):
      with self.subTest(name=name):
        own = dict.__getitem__(space, name)
        self.assertEqual(own.__name__, name)
        with self.assertRaises(ReservedName) as context:
          space[name] = other
        self.assertEqual(context.exception.resName, name)
        expected = "Attempted to use reserved name: '%s'!" % name
        self.assertEqual(str(context.exception), expected)
        self.assertIs(dict.__getitem__(space, name), own)
        space.__setitem__(name, other, _root=True)
        self.assertIs(dict.__getitem__(space, name), other)
    space['helper'] = other
    self.assertIs(dict.__getitem__(space, 'helper'), other)

  def test_debug_in_class_body_refused(self) -> None:
    reached = []
    with self.assertRaises(ReservedName) as context:
      class Case(BaseTest):
        reached.append('before')
        debug = True
        reached.append('after')  # pragma: no cover

    self.assertEqual(context.exception.resName, 'debug')
    expected = "Attempted to use reserved name: 'debug'!"
    self.assertEqual(str(context.exception), expected)
    self.assertEqual(reached, ['before'])

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

  def test_do_cleanups_in_class_body_refused(self) -> None:
    reached = []
    with self.assertRaises(ReservedName) as context:
      class Case(BaseTest):
        reached.append('before')

        def doCleanups(self) -> None:
          """Never runs: the line that binds it is refused."""

        reached.append('after')  # pragma: no cover

    self.assertEqual(context.exception.resName, 'doCleanups')
    expected = "Attempted to use reserved name: 'doCleanups'!"
    self.assertEqual(str(context.exception), expected)
    #  The refusal comes at the line of the class body that binds the
    #  name, so the class body goes no further.
    self.assertEqual(reached, ['before'])

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
    self.assertEqual(len(result.failures), 1)
    self.assertEqual(result.errors, [])
    self.assertIn('FAIL [n=1]: 1 != 2', result.failures[0][1])
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

    result = self._run(Case)
    self.assertEqual(len(result.failures), 1)
    self.assertEqual(result.errors, [])
    self.assertIn('FAIL [n=1]: 1 != 2', result.failures[0][1])
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

    result = self._run(Case)
    self.assertEqual(len(result.failures), 1)
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
    self.assertEqual(len(result.failures), 1)
    self.assertEqual(result.errors, [])
