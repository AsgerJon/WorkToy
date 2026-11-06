"""
TestSignals tests 'ControlFlow' and 'SkipSet' from
'worktoy.core.control_flow' and the declaration of a signal.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.control_flow import ControlFlow, SkipSet
from worktoy.waitaminute import WorkToyException
from worktoy.waitaminute.meta import ControlClassError
from . import CoreTest, Nudge


class TestSignals(CoreTest):
  """
  A control-flow signal steers a protocol rather than reporting a
  failure: 'except ControlFlow' catches every signal, no signal is a
  'WorkToyException', and a signal carries nothing but its type and an
  optional text. The tests pin the catch, the separation from errors,
  a signal of a project with its own text, and the refusals of a body
  defining anything else.
  """

  def test_root_catches_every_signal(self) -> None:
    for signal in (SkipSet, Nudge, ControlFlow):
      with self.subTest(signal=signal.__name__):
        with self.assertRaises(ControlFlow) as context:
          raise signal
        self.assertEqual(context.exception.args, ())
        self.assertIsSubclass(signal, Exception)

  def test_not_an_error(self) -> None:
    self.assertIsNotSubclass(SkipSet, WorkToyException)
    self.assertIsNotInstance(SkipSet(), WorkToyException)

  def test_text_ignores_arguments(self) -> None:
    self.assertEqual(SkipSet('reason').args, ('reason',))
    self.assertEqual(str(SkipSet('reason')), '<ControlFlow: SkipSet>')

  def test_project_signal_with_own_text(self) -> None:
    self.assertEqual(str(Nudge()), 'nudge!')
    self.assertEqual(str(Nudge), '<ControlFlow: Nudge>')
    self.assertIs(Nudge.__is_root__, False)
    self.assertIn("'Nudge' does both", Nudge.__doc__)

  def test_docstring_only_body(self) -> None:
    class CORE_SIG(ControlFlow):
      """A signal with a docstring alone."""

    self.assertEqual(CORE_SIG.__doc__, 'A signal with a docstring alone.')
    self.assertEqual(str(CORE_SIG), '<ControlFlow: CORE_SIG>')

  def test_body_with_method_refused(self) -> None:
    with self.assertRaises(ControlClassError) as context:
      class Bad(ControlFlow):
        def act(self) -> None:
          """A method a signal may not hold."""
    self.assertEqual(context.exception.badKey, 'act')
    self.assertEqual(context.exception.space.__class_name__, 'Bad')
    self.assertIn("'Bad'", str(context.exception))
    self.assertIn("binds 'act'", str(context.exception))
    self.assertEqual(context.exception.space.__class_name__, 'Bad')

  def test_body_with_state_refused(self) -> None:
    with self.assertRaises(ControlClassError) as context:
      class Bad(ControlFlow):
        value = 1
    self.assertEqual(context.exception.badKey, 'value')
    self.assertEqual(context.exception.space.__class_name__, 'Bad')
    self.assertIn("binds 'value'", str(context.exception))

  def test_body_with_init_refused(self) -> None:
    with self.assertRaises(ControlClassError) as context:
      class Bad(ControlFlow):
        def __init__(self) -> None:
          """A constructor a signal may not hold."""
    self.assertEqual(context.exception.badKey, '__init__')
    self.assertEqual(context.exception.space.__class_name__, 'Bad')
    self.assertIn("binds '__init__'", str(context.exception))
