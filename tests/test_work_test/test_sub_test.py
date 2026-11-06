"""
TestSubTest tests 'SubTest' from 'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import SkipTest

from worktoy.waitaminute import TypeException
from worktoy.work_test import BaseTest, SubTest
from . import WorkTestTest


class TestSubTest(WorkTestTest):
  """
  'SubTest' is the accumulator behind 'self.subTest' in every test of
  the suite: a block records what it raised under its label and lets the
  test run on. The tests take one accumulator apart on its own: the
  labels a call and a bare block push and the chain of nested blocks,
  the records of passed, failed and errored blocks with their labels,
  the signals it lets through, its truth, the descriptor through the
  class and through an instance with the peek and the refusal of a
  stray value, the refusals of its own stores, and the framed report.
  """

  def test_labels(self) -> None:
    sub = SubTest()
    self.assertEqual(sub.current, '<sub test>')
    self.assertIsNone(sub.__current_tests__)
    with sub(x=1):
      self.assertEqual(sub.current, 'x=1')
      with sub(2, y=3):
        self.assertEqual(sub.current, 'x=1 -> 2, y=3')
      self.assertEqual(sub.current, 'x=1')
      with sub:
        self.assertEqual(sub.current, 'x=1 -> <sub test>')
      self.assertEqual(sub.current, 'x=1')
    self.assertEqual(sub.current, '<sub test>')
    self.assertIsNone(sub.__current_tests__)
    with sub('a', 'b'):
      self.assertEqual(sub.current, 'a, b')
    with sub:
      self.assertEqual(sub.current, '<sub test>')
    self.assertEqual(sub.passed, ('x=1 -> 2, y=3', 'x=1 -> <sub test>',
                                  'x=1', 'a, b', '<sub test>'))
    with sub(a=1):
      with sub(b=2):
        with sub(c=3):
          self.assertEqual(sub.current, 'a=1 -> b=2 -> c=3')
        self.assertEqual(sub.current, 'a=1 -> b=2')
        self.assertEqual(sub.__current_tests__, ('a=1', 'b=2'))
      self.assertEqual(sub.current, 'a=1')
    self.assertEqual(sub.current, '<sub test>')

  def test_records(self) -> None:
    sub = SubTest()
    self.assertEqual((sub.fails, sub.errors, sub.passed), ((), (), ()))
    self.assertEqual((sub.failLabels, sub.errorLabels), ((), ()))
    self.assertFalse(sub)
    with sub(step=1):
      raise AssertionError('one')
    self.assertTrue(sub)
    with sub(step=2):
      raise KeyError('two')
    with sub(step=3):
      pass
    self.assertEqual([str(fail) for fail in sub.fails], ['one'])
    self.assertEqual(sub.failLabels, ('step=1',))
    self.assertEqual([repr(error) for error in sub.errors],
                     ["KeyError('two')"])
    self.assertEqual(sub.errorLabels, ('step=2',))
    self.assertEqual(sub.passed, ('step=3',))
    self.assertEqual(sub.current, '<sub test>')
    self.assertTrue(sub)
    errored = SubTest()
    with errored:
      raise ValueError('lone')
    self.assertTrue(errored)
    self.assertEqual(errored.errorLabels, ('<sub test>',))
    self.assertEqual(errored.fails, ())
    self.assertIn('| status   :  FAILED', repr(errored))
    self.assertNotIn('.. and', repr(errored))
    failed = SubTest()
    with failed:
      raise AssertionError('lone')
    self.assertTrue(failed)
    self.assertEqual(failed.failLabels, ('<sub test>',))
    self.assertEqual(failed.errors, ())
    self.assertIn('| status   :  FAILED', repr(failed))
    self.assertNotIn('.. and', repr(failed))

  def test_signals_pass_through(self) -> None:
    sub = SubTest()
    with self.assertRaises(SkipTest) as context:
      with sub(step=1):
        raise SkipTest('later')
    self.assertEqual(str(context.exception), 'later')
    self.assertEqual(sub.current, '<sub test>')

    class Halt(BaseException):
      """A signal that is no 'Exception'."""

    with self.assertRaises(Halt) as context:
      with sub(step=2):
        raise Halt('now')
    self.assertEqual(context.exception.args, ('now',))
    self.assertEqual(sub.current, '<sub test>')
    self.assertEqual((sub.fails, sub.errors, sub.passed), ((), (), ()))
    self.assertFalse(sub)

  def test_descriptor(self) -> None:
    descriptor = BaseTest.__dict__['subTest']
    self.assertIsInstance(descriptor, SubTest)
    self.assertIs(BaseTest.subTest, descriptor)
    self.assertEqual(descriptor.__field_name__, 'subTest')
    self.assertIs(descriptor.__field_owner__, BaseTest)

    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the case is built for its descriptor alone."""

    case = Case('test_nothing')
    with self.assertRaises(RecursionError) as context:
      Case.subTest.__get__(case, Case, _recursion=True)
    self.assertEqual(context.exception.args, ())
    sub = case.subTest
    self.assertIsInstance(sub, SubTest)
    self.assertIs(case.subTest, sub)
    self.assertIs(case.__dict__['__sub_test__'], sub)
    self.assertIs(sub.__owning_instance__, case)
    self.assertIs(sub.__owning_test__, Case)
    self.assertEqual(sub.__field_name__, '__sub_test__')
    self.assertIs(sub.__field_owner__, Case)
    self.assertIs(Case.subTest.__get__(case, Case, _recursion=True), sub)
    self.assertIsNot(Case('test_nothing').subTest, sub)
    object.__setattr__(case, '__sub_test__', 5)
    with self.assertRaises(TypeException) as context:
      _ = case.subTest
    self.assertTypeRefused(context.exception, '__sub_test__', 5, SubTest)

  def test_stores_refused(self) -> None:
    sub = SubTest()
    sub.__test_fails__ = ('x',)
    with self.assertRaises(TypeException) as context:
      _ = sub.fails
    self.assertTypeRefused(context.exception, 'fail', 'x', AssertionError)
    sub.__test_fails__ = 'x'
    with self.assertRaises(TypeException) as context:
      _ = sub.fails
    self.assertTypeRefused(context.exception, '__test_fails__', 'x', tuple)
    sub.__test_errors__ = ('x',)
    with self.assertRaises(TypeException) as context:
      _ = sub.errors
    self.assertTypeRefused(context.exception, 'error', 'x', Exception)
    sub.__test_errors__ = 'x'
    with self.assertRaises(TypeException) as context:
      _ = sub.errors
    self.assertTypeRefused(context.exception, '__test_errors__', 'x', tuple)
    sub.__test_passed__ = (1,)
    with self.assertRaises(TypeException) as context:
      _ = sub.passed
    self.assertTypeRefused(context.exception, 'passed', 1, str)
    sub.__test_passed__ = 'x'
    with self.assertRaises(TypeException) as context:
      _ = sub.passed
    self.assertTypeRefused(context.exception, '__test_passed__', 'x', tuple)
    fresh = SubTest()
    for getter in (fresh._getFails, fresh._getErrors, fresh._getPassed):
      with self.subTest(getter=getter.__name__):
        with self.assertRaises(RecursionError) as context:
          getter(_recursion=True)
        self.assertEqual(context.exception.args, ())
    self.assertEqual((fresh.fails, fresh.errors, fresh.passed), ((), (), ()))
    with self.assertRaises(TypeException) as context:
      fresh.current = 5
    self.assertTypeRefused(context.exception, 'current', 5, str)
    with self.assertRaises(RuntimeError) as context:
      fresh._popCurrent()
    self.assertEqual(str(context.exception), "'SubTest' has no label to "
                                             "remove: '__exit__' ran "
                                             "without a matching "
                                             "'__enter__'!")

  def test_report(self) -> None:
    sub = SubTest()
    text = repr(sub)
    self.assertEqual(str(sub), text)
    lines = text.split('\n')
    self.assertEqual(len(lines), 7)
    self.assertEqual(lines[0], '+' + '=' * 62 + '+')
    title = '.  SubTest  .   runTest'
    self.assertEqual(lines[1], '| %s |' % title.center(60))
    self.assertEqual(lines[2], lines[0])
    self.assertEqual(lines[3], '| %s |' % 'status   :  IDLE'.ljust(60))
    self.assertEqual(lines[4], '| %s |' % 'active   :  <none>'.ljust(60))
    totals = 'totals   :  0 passed   0 failed   0 errored'
    self.assertEqual(lines[5], '| %s |' % totals.ljust(60))
    self.assertEqual(lines[6], lines[0])
    with sub(step=1):
      pass
    self.assertIn('| status   :  PASSED', repr(sub))
    self.assertIn('|    +  step=1', repr(sub))
    self.assertNotIn('.. and', repr(sub))
    with sub(step=2):
      self.assertIn('| active   :  step=2', repr(sub))
      raise AssertionError('oops')
    with sub(step=3):
      raise ValueError('bad')
    text = repr(sub)
    self.assertIn('| status   :  FAILED', text)
    self.assertIn('| totals   :  1 passed   1 failed   1 errored', text)
    self.assertIn('|    x  [step=2] oops', text)
    self.assertIn("|    !  [step=3] ValueError('bad')", text)
    self.assertEqual(text.count('+' + '-' * 62 + '+'), 3)
    with sub(label='x' * 80):
      pass
    for n in range(9):
      with sub(n=n):
        pass
      with sub(n=n):
        raise AssertionError(str(n))
      with sub(n=n):
        raise KeyError(n)
    text = repr(sub)
    self.assertEqual(text.count('.. and 2 more'), 2)
    self.assertEqual(text.count('.. and 3 more'), 1)
    for line in text.split('\n'):
      with self.subTest(line=line):
        self.assertEqual(len(line), 64)
    self.assertIn('|    +  label=' + 'x' * 45 + '... |', text)
    self.assertIn('| totals   :  11 passed   10 failed   10 errored', text)
    self.assertEqual(self._rows(text), (8, 8, 8))

  def test_report_shows_eight_of_each(self) -> None:
    for count, more in ((7, None), (8, None), (9, 1), (17, 9)):
      with self.subTest(count=count):
        sub = SubTest()
        for n in range(count):
          with sub(n=n):
            pass
          with sub(n=n):
            raise AssertionError(str(n))
          with sub(n=n):
            raise KeyError(n)
        text = repr(sub)
        shown = min(count, 8)
        self.assertEqual(self._rows(text), (shown, shown, shown))
        self.assertEqual(text.count('.. and'), 0 if more is None else 3)
        self.assertEqual(text.count('.. and %s more' % more),
                         0 if more is None else 3)
        totals = '| totals   :  %d passed   %d failed   %d errored'
        self.assertIn(totals % (count, count, count), text)

  @staticmethod
  def _rows(text: str) -> tuple:
    """The rows of passes, fails and errors the report shows."""
    lines = text.split('\n')
    return (len([l for l in lines if l.startswith('|    +  ')]),
            len([l for l in lines if l.startswith('|    x  ')]),
            len([l for l in lines if l.startswith('|    !  ')]))

  def test_report_names_the_owning_test(self) -> None:
    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the case is built for its report alone."""

    case = Case('test_nothing')
    self.assertIn('.  SubTest  .   Case', repr(case.subTest))
    self.assertNotIn('runTest', repr(case.subTest))
