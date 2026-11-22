"""
PromiseControlFlow promises the signals of 'worktoy.core.control_flow'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.control_flow import ControlFlow, SkipSet
from worktoy.waitaminute import WorkToyException


class PromiseControlFlow(TestCase):
  """
  A control-flow signal is an exception that steers a protocol rather than
  reporting a failure, as 'StopIteration' does. Every signal is a subclass of
  'ControlFlow', so 'except ControlFlow' catches them all, and none is a
  'WorkToyException', so a signal is never taken for an error. 'SkipSet' is
  one. A project declares a signal of its own with a class statement on
  'ControlFlow' whose body holds a docstring and, if it likes, '__str__' and
  '__repr__'. Source: the docstrings of the 'control_flow' package,
  'ControlFlow', 'SkipSet', 'MetaFlow' and 'ControlSpace', and the 1.1.0
  changelog entry "A control-flow signal body may not bind __namespace__".
  """

  def test_family(self) -> None:
    self.assertTrue(issubclass(SkipSet, ControlFlow))
    self.assertTrue(issubclass(ControlFlow, Exception))
    self.assertFalse(issubclass(ControlFlow, WorkToyException))

  def test_own_signal(self) -> None:
    class Retry(ControlFlow):
      """The step should run again."""

    caught = None
    try:
      raise Retry
    except ControlFlow as signal:
      caught = signal
    self.assertIsInstance(caught, Retry)

  def test_own_text(self) -> None:
    class Done(ControlFlow):
      """The work is done."""

      def __str__(self) -> str:
        return 'done'

    self.assertEqual(str(Done()), 'done')
