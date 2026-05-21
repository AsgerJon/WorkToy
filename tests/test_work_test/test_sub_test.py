"""
TestSubTest tests the 'SubTest' class of 'worktoy.work_test'. Covers
the collector buckets, the nested-label stack, the context-manager
protocol, the descriptor mechanics, and the framed repr.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest, SubTest
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSubTest(BaseTest):
  """
  Exercises the standalone behaviour of 'SubTest' instances without
  going through the descriptor on 'BaseTest', so the cute repr and
  internal state machine can be probed in isolation.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  BUCKETS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_lazy_init_fails(self) -> None:
    """Accessing 'fails' before any block runs returns empty tuple."""
    sub = SubTest()
    self.assertEqual(sub.fails, ())

  def test_lazy_init_errors(self) -> None:
    """Accessing 'errors' before any block runs returns empty tuple."""
    sub = SubTest()
    self.assertEqual(sub.errors, ())

  def test_lazy_init_passed(self) -> None:
    """Accessing 'passed' before any block runs returns empty tuple."""
    sub = SubTest()
    self.assertEqual(sub.passed, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CURRENT / STACK  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_current_fallback(self) -> None:
    """Before any block, 'current' returns the fallback string."""
    sub = SubTest()
    self.assertEqual(sub.current, '<sub test>')

  def test_call_pushes_positional_args(self) -> None:
    """Positional args are rendered in the label."""
    sub = SubTest()
    with sub('foo', 42):
      self.assertEqual(sub.current, 'foo, 42')

  def test_call_pushes_kwargs(self) -> None:
    """Keyword args are rendered as 'k=v' pairs in the label."""
    sub = SubTest()
    with sub(target='x'):
      self.assertEqual(sub.current, 'target=x')

  def test_call_mixes_args_and_kwargs(self) -> None:
    """Positional and keyword args both appear in the label."""
    sub = SubTest()
    with sub('foo', target='x'):
      self.assertEqual(sub.current, 'foo, target=x')

  def test_call_with_no_args(self) -> None:
    """Empty call produces an empty label string."""
    sub = SubTest()
    with sub():
      self.assertEqual(sub.current, '')

  def test_nested_blocks_chain(self) -> None:
    """Nested entry chains labels with ' -> '."""
    sub = SubTest()
    with sub('outer'):
      with sub('inner'):
        self.assertEqual(sub.current, 'outer -> inner')

  def test_nested_pop_restores_outer(self) -> None:
    """Exiting an inner block restores the outer label."""
    sub = SubTest()
    with sub('outer'):
      with sub('inner'):
        pass
      self.assertEqual(sub.current, 'outer')

  def test_current_resets_after_outermost_exit(self) -> None:
    """After the outermost exit the stack returns to fallback."""
    sub = SubTest()
    with sub('one'):
      pass
    self.assertEqual(sub.current, '<sub test>')

  def test_set_current_wrong_type_raises(self) -> None:
    """Assigning a non-str to 'current' raises TypeException."""
    sub = SubTest()
    with self.assertRaises(TypeException):
      sub.current = 42

  def test_pop_underflow_raises(self) -> None:
    """Popping with an empty stack raises RuntimeError."""
    sub = SubTest()
    with self.assertRaises(RuntimeError):
      sub._popCurrent()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONTEXT MANAGER EXIT  # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_passing_block_recorded(self) -> None:
    """A block that does not raise gets recorded in 'passed'."""
    sub = SubTest()
    with sub('foo'):
      pass
    self.assertEqual(sub.passed, ('foo',))
    self.assertEqual(sub.fails, ())
    self.assertEqual(sub.errors, ())

  def test_failing_block_recorded(self) -> None:
    """A block that raises AssertionError records it in 'fails'."""
    sub = SubTest()
    try:
      with sub('foo'):
        raise AssertionError('bad')
    finally:
      self.assertEqual(len(sub.fails), 1)
      self.assertIsInstance(sub.fails[0], AssertionError)
      self.assertEqual(sub.passed, ())
      self.assertEqual(sub.errors, ())

  def test_erroring_block_recorded(self) -> None:
    """A block that raises non-AssertionError records it in 'errors'."""
    sub = SubTest()
    try:
      with sub('foo'):
        raise ValueError('nope')
    finally:
      self.assertEqual(len(sub.errors), 1)
      self.assertIsInstance(sub.errors[0], ValueError)
      self.assertEqual(sub.passed, ())
      self.assertEqual(sub.fails, ())

  def test_base_exception_propagates(self) -> None:
    """BaseException subclasses outside Exception propagate unswallowed."""
    sub = SubTest()
    with self.assertRaises(KeyboardInterrupt):
      with sub('foo'):
        raise KeyboardInterrupt

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  __bool__   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_bool_idle_is_false(self) -> None:
    """Idle sub test is falsy."""
    sub = SubTest()
    self.assertFalse(bool(sub))

  def test_bool_after_pass_is_false(self) -> None:
    """A sub test with only passes is falsy."""
    sub = SubTest()
    with sub('foo'):
      pass
    self.assertFalse(bool(sub))

  def test_bool_after_fail_is_true(self) -> None:
    """A sub test with any fail is truthy."""
    sub = SubTest()
    with sub('foo'):
      raise AssertionError
    self.assertTrue(bool(sub))

  def test_bool_after_error_is_true(self) -> None:
    """A sub test with any error is truthy."""
    sub = SubTest()
    with sub('foo'):
      raise ValueError
    self.assertTrue(bool(sub))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  __repr__   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_repr_idle_status(self) -> None:
    """Idle sub test reports status IDLE."""
    sub = SubTest()
    self.assertIn('IDLE', repr(sub))

  def test_repr_passed_status(self) -> None:
    """Sub test with only passes reports status PASSED."""
    sub = SubTest()
    with sub('foo'):
      pass
    self.assertIn('PASSED', repr(sub))

  def test_repr_failed_status_for_fail(self) -> None:
    """A fail flips status to FAILED."""
    sub = SubTest()
    try:
      with sub('foo'):
        raise AssertionError('x')
    finally:
      self.assertIn('FAILED', repr(sub))

  def test_repr_failed_status_for_error(self) -> None:
    """An error also flips status to FAILED."""
    sub = SubTest()
    try:
      with sub('foo'):
        raise RuntimeError('e')
    finally:
      self.assertIn('FAILED', repr(sub))

  def test_repr_includes_class_name(self) -> None:
    """The framed banner contains the type name."""
    sub = SubTest()
    self.assertIn('SubTest', repr(sub))

  def test_repr_active_label_shown(self) -> None:
    """When the stack is non-empty, the chain is visible."""
    sub = SubTest()
    sub.current = 'live label'
    self.assertIn('live label', repr(sub))

  def test_repr_truncates_long_rows(self) -> None:
    """Rows longer than the inner width get an ellipsis."""
    sub = SubTest()
    longLabel = 'x' * 200
    with sub(longLabel):
      pass
    self.assertIn('...', repr(sub))

  def test_repr_caps_long_passed_list(self) -> None:
    """The passes section is capped at 8 entries with a 'more' tail."""
    sub = SubTest()
    for i in range(15):
      with sub('iter %d' % i):
        pass
    self.assertIn('more', repr(sub))

  def test_repr_caps_long_fails_list(self) -> None:
    """The fails section is capped at 8 entries with a 'more' tail."""
    sub = SubTest()
    for i in range(15):
      with sub('iter %d' % i):
        raise AssertionError('boom %d' % i)
    self.assertIn('more', repr(sub))

  def test_repr_caps_long_errors_list(self) -> None:
    """The errors section is capped at 8 entries with a 'more' tail."""
    sub = SubTest()
    for i in range(15):
      with sub('iter %d' % i):
        raise ValueError('nope %d' % i)
    self.assertIn('more', repr(sub))

  def test_str_equals_repr(self) -> None:
    """'str' and 'repr' share the same implementation."""
    sub = SubTest()
    self.assertEqual(str(sub), repr(sub))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DESCRIPTOR MECHANICS    # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_class_access_returns_descriptor(self) -> None:
    """Accessing the 'subTest' attribute on the class returns it."""
    desc = BaseTest.subTest
    self.assertIsInstance(desc, SubTest)

  def test_instance_access_lazily_creates_copy(self) -> None:
    """Accessing 'subTest' on an instance creates a per-instance copy."""
    inst = TestSubTest('test_lazy_init_fails')
    sub = inst.subTest
    self.assertIsInstance(sub, SubTest)
    self.assertIsNot(sub, BaseTest.subTest)

  def test_per_instance_copies_are_distinct(self) -> None:
    """Two owning instances get two different SubTest copies."""
    instA = TestSubTest('test_lazy_init_fails')
    instB = TestSubTest('test_lazy_init_fails')
    self.assertIsNot(instA.subTest, instB.subTest)

  def test_recursion_sentinel_raises_when_missing(self) -> None:
    """Peek with _recursion=True raises RecursionError on missing attr."""
    inst = TestSubTest('test_lazy_init_fails')
    with self.assertRaises(RecursionError):
      type(inst).subTest.__get__(inst, type(inst), _recursion=True)

  def test_recursion_sentinel_returns_after_creation(self) -> None:
    """Once 'subTest' has been accessed, the peek returns the copy."""
    inst = TestSubTest('test_lazy_init_fails')
    created = inst.subTest
    peeked = type(inst).subTest.__get__(inst, type(inst), _recursion=True)
    self.assertIs(created, peeked)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PEDANTIC GETTER BRANCHES   # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_get_fails_recursion_sentinel(self) -> None:
    """_getFails with _recursion=True on uninitialized state raises."""
    sub = SubTest()
    with self.assertRaises(RecursionError):
      sub._getFails(_recursion=True)

  def test_get_fails_wrong_element_type(self) -> None:
    """A poisoned 'fails' tuple raises TypeException on read."""
    sub = SubTest()
    sub.__test_fails__ = (AssertionError('ok'), 'not-an-exception')  # noqa
    with self.assertRaises(TypeException):
      _ = sub.fails

  def test_get_fails_non_tuple_state(self) -> None:
    """Setting '__test_fails__' to a non-tuple, non-None raises."""
    sub = SubTest()
    sub.__test_fails__ = 'not-a-tuple'  # noqa
    with self.assertRaises(TypeException):
      _ = sub.fails

  def test_get_errors_recursion_sentinel(self) -> None:
    """_getErrors with _recursion=True on uninitialized state raises."""
    sub = SubTest()
    with self.assertRaises(RecursionError):
      sub._getErrors(_recursion=True)

  def test_get_errors_wrong_element_type(self) -> None:
    """A poisoned 'errors' tuple raises TypeException on read."""
    sub = SubTest()
    sub.__test_errors__ = (ValueError('ok'), 'not-an-exception')  # noqa
    with self.assertRaises(TypeException):
      _ = sub.errors

  def test_get_errors_non_tuple_state(self) -> None:
    """Setting '__test_errors__' to a non-tuple, non-None raises."""
    sub = SubTest()
    sub.__test_errors__ = 42  # noqa
    with self.assertRaises(TypeException):
      _ = sub.errors

  def test_get_passed_recursion_sentinel(self) -> None:
    """_getPassed with _recursion=True on uninitialized state raises."""
    sub = SubTest()
    with self.assertRaises(RecursionError):
      sub._getPassed(_recursion=True)

  def test_get_passed_wrong_element_type(self) -> None:
    """A poisoned 'passed' tuple raises TypeException on read."""
    sub = SubTest()
    sub.__test_passed__ = ('ok', 42)  # noqa
    with self.assertRaises(TypeException):
      _ = sub.passed

  def test_get_passed_non_tuple_state(self) -> None:
    """Setting '__test_passed__' to a non-tuple, non-None raises."""
    sub = SubTest()
    sub.__test_passed__ = ['list', 'not', 'tuple']  # noqa
    with self.assertRaises(TypeException):
      _ = sub.passed

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STR AND REPR # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_str_repr(self, ) -> None:
    """'str' and 'repr' share the same implementation."""

    class _Test(BaseTest):
      pass

    class _Test2(_Test):
      _testMethodName = 'runTest'

    class _Test3(_Test):
      _testMethodName = 'trolololo'

    _test = _Test()
    _test2 = _Test2()
    _test3 = _Test3()
    self.assertEqual(str(_test.subTest), repr(_test.subTest))
    self.assertEqual(str(_test2.subTest), repr(_test2.subTest))
    self.assertEqual(str(_test3.subTest), repr(_test3.subTest))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NONE-DESCRIPTOR  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_owner_is_none(self, ) -> None:
    """A SubTest instance can be used without an owning class."""
    sub = SubTest()
    self.assertEqual(str(sub), repr(sub))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  BAD TYPE   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_bad_type(self, ) -> None:
    """Covering the bad type branch at the private name"""

    _test = BaseTest()
    pvtName = SubTest.__private_name__
    sus = object()
    object.__setattr__(_test, pvtName, sus)
    with self.assertRaises(TypeException) as context:
      _ = _test.subTest
    e = context.exception
    self.assertIs(e.actualObject, sus)
    self.assertIs(e.actualType, object)
    self.assertEqual(e.varName, pvtName)
    self.assertIn(SubTest, e.expectedTypes)
