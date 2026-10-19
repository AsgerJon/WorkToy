"""
TestReservedNameSyntax subclasses 'WaitAMinuteTest' and pins that
'ReservedName' is a 'SyntaxError', as every other refusal of a class-body
line is, with its message on 'msg' so a traceback shows it. It used to be
the one such refusal based on 'Exception', so 'except SyntaxError' around
a class statement caught a near-miss dunder but not a reassigned
'__doc__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy.mcls import BaseObject
from worktoy.waitaminute import WorkToyException
from worktoy.waitaminute.meta import ReservedName

from . import WaitAMinuteTest


class TestReservedNameSyntax(WaitAMinuteTest):
  """
  TestReservedNameSyntax provides tests for the bases and message of
  'ReservedName'.
  """

  def test_bases_and_message(self) -> None:
    """A 'SyntaxError' and a 'WorkToyException', naming the name on
    'resName' and in 'msg'."""
    e = ReservedName('__module__')
    self.assertIsInstance(e, SyntaxError)
    self.assertIsInstance(e, WorkToyException)
    self.assertEqual(e.resName, '__module__')
    self.assertEqual(e.msg, str(e))
    self.assertIn("'__module__'", str(e))
    self.assertEqual(str(e), repr(e))

  def test_caught_as_syntax_error(self) -> None:
    """A class statement reassigning a reserved name is caught by
    'except SyntaxError'."""
    with self.assertRaises(SyntaxError) as context:
      class Owner(BaseObject):
        __module__ = 'elsewhere'
    self.assertIsInstance(context.exception, ReservedName)

  def test_round_trip(self) -> None:
    """It pickles through the common base."""
    back = pickle.loads(pickle.dumps(ReservedName('__doc__')))
    self.assertEqual(back.resName, '__doc__')
    self.assertEqual(back.msg, str(back))
