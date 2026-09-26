"""
TestSubTestBare subclasses 'BaseTest' and pins that a 'SubTest' also
works as a context manager without being called first. A bare block, as
in 'with self.subTest:', is recorded under the fallback label
'<sub test>' exactly as a called block is recorded under its own label,
and it leaves whatever the block raised untouched. Nested in a called
block, or holding one, it takes its place in the chain of labels.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import BaseTest, SubTest


class TestSubTestBare(BaseTest):
  """
  TestSubTestBare provides tests for 'SubTest' blocks entered without a
  call.
  """

  def test_bare_block_passes(self) -> None:
    """A bare block that raises nothing is recorded as passed under the
    fallback label, and the label is gone once the block ends."""
    sub = SubTest()
    with sub:
      self.assertEqual(sub.current, '<sub test>')
    self.assertEqual(sub.passed, ('<sub test>',))
    self.assertEqual(sub.fails, ())
    self.assertEqual(sub.errors, ())
    self.assertEqual(sub.current, '<sub test>')

  def test_bare_block_records_fail(self) -> None:
    """An 'AssertionError' in a bare block is recorded as a fail and goes
    no further."""
    sub = SubTest()
    with sub:
      raise AssertionError('bare fail')
    self.assertEqual([str(fail) for fail in sub.fails], ['bare fail'])
    self.assertEqual(sub.passed, ())

  def test_bare_block_records_error(self) -> None:
    """Any other exception in a bare block is recorded as an error and
    goes no further."""
    sub = SubTest()
    with sub:
      raise ValueError('bare error')
    self.assertEqual([str(error) for error in sub.errors], ['bare error'])
    self.assertEqual(sub.passed, ())

  def test_bare_block_keeps_base_exception(self) -> None:
    """A 'BaseException' that is not an 'Exception' leaves a bare block as
    itself."""
    sub = SubTest()
    with self.assertRaises(KeyboardInterrupt):
      with sub:
        raise KeyboardInterrupt

  def test_bare_inside_called(self) -> None:
    """A bare block inside a called one adds the fallback label to the
    chain and leaves the outer label in place."""
    sub = SubTest()
    with sub('outer'):
      with sub:
        self.assertEqual(sub.current, 'outer -> <sub test>')
      self.assertEqual(sub.current, 'outer')
    self.assertEqual(sub.passed, ('outer -> <sub test>', 'outer'))

  def test_called_inside_bare(self) -> None:
    """A called block inside a bare one chains its label after the
    fallback label."""
    sub = SubTest()
    with sub:
      with sub('inner'):
        self.assertEqual(sub.current, '<sub test> -> inner')
    self.assertEqual(sub.passed, ('<sub test> -> inner', '<sub test>'))

  def test_bare_through_descriptor(self) -> None:
    """The per-test 'SubTest' on a 'BaseTest' works bare too."""
    other = type(self)(self._testMethodName)
    with other.subTest:
      pass
    self.assertEqual(other.subTest.passed, ('<sub test>',))

  def test_underflow_message(self) -> None:
    """Leaving a block that was never entered raises 'RuntimeError' with a
    message saying so, rather than an empty one."""
    sub = SubTest()
    with self.assertRaises(RuntimeError) as context:
      sub._popCurrent()
    self.assertIn('__enter__', str(context.exception))
