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
  'TestMeta' is a metaclass a test base may choose, with 'TestSpace' as
  its namespace. It puts the library's own 'doCleanups' and 'debug' into
  the namespace of each class it builds before the class body runs, and
  the namespace refuses the line of a class body that binds either
  name. 'BaseTest' itself is not built by it. The tests pin the two
  classes, the two methods in every class 'TestMeta' builds, the
  namespace, the refusal of each name at its line, and that a test class
  it builds reports its failed 'subTest' blocks under 'run' and under
  'debug'.
  """

  @staticmethod
  def makeStrict() -> type:
    """A test base built by 'TestMeta'."""

    class Strict(BaseTest, metaclass=work_test.TestMeta):
      """Its test classes bind neither 'doCleanups' nor 'debug'."""

    return Strict

  def test_shape(self) -> None:
    Strict = self.makeStrict()

    class Case(Strict):
      def test_nothing(self) -> None:
        """Never runs: the class is built for its namespace alone."""

    self.assertIsSubclass(work_test.TestMeta, BaseMeta)
    self.assertIsSubclass(work_test.TestSpace, BaseSpace)
    self.assertIsNot(type(BaseTest), work_test.TestMeta)
    for cls in (Strict, Case):
      with self.subTest(cls=cls.__name__):
        self.assertIs(type(cls), work_test.TestMeta)
        for name in ('doCleanups', 'debug'):
          self.assertEqual(vars(cls)[name].__name__, name)
    #  The factories take no receiver, read through a class as well.
    self.assertEqual(Strict._doCleanupsFactory().__name__, 'doCleanups')
    self.assertEqual(Strict._debugFactory().__name__, 'debug')

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
    Strict = self.makeStrict()
    reached = []
    with self.assertRaises(ReservedName) as context:
      class Case(Strict):
        reached.append('before')
        debug = True
        reached.append('after')  # pragma: no cover

    self.assertEqual(context.exception.resName, 'debug')
    expected = "Attempted to use reserved name: 'debug'!"
    self.assertEqual(str(context.exception), expected)
    self.assertEqual(reached, ['before'])

  def test_do_cleanups_in_class_body_refused(self) -> None:
    Strict = self.makeStrict()
    reached = []
    with self.assertRaises(ReservedName) as context:
      class Case(Strict):
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

  def test_report_of_a_class_it_builds(self) -> None:
    Strict = self.makeStrict()

    class Case(Strict):
      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)

      def test_fine(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 1)

    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(Case).run(result)
    self.assertEqual(result.testsRun, 2)
    self.assertEqual(len(result.failures), 1)
    self.assertEqual(result.errors, [])
    self.assertIn('FAIL [n=1]: 1 != 2', result.failures[0][1])
    with self.assertRaises(AssertionError) as context:
      Case('test_block').debug()
    self.assertIn('FAIL [n=1]: 1 != 2', str(context.exception))
    self.assertIsNone(Case('test_fine').debug())
