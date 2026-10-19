"""
TestControlFlowReexport subclasses 'WaitAMinuteTest' and pins that
'worktoy.waitaminute.control_flow' is a thin re-export of the control-flow
family, which now lives in 'worktoy.core.control_flow' beside the
sentinels, with 'ControlClassError' in 'worktoy.waitaminute.meta' among
the other class-body refusals. The old path keeps working for the 1.x
releases; the names are resolved on access, so importing 'waitaminute'
does not import 'core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import core, waitaminute
from worktoy.core import control_flow
from worktoy.core.control_flow import ControlFlow, SkipSet
from worktoy.core.control_flow import MetaFlow, ControlSpace
from worktoy.waitaminute import control_flow as reexport
from worktoy.waitaminute.meta import ControlClassError

from . import WaitAMinuteTest


class TestControlFlowReexport(WaitAMinuteTest):
  """
  TestControlFlowReexport provides tests for the moved control-flow
  family and its re-export.
  """

  def test_lives_in_core(self) -> None:
    """The family is a subpackage of 'core', listed beside the
    sentinels, and the signal is the one 'Object' catches."""
    self.assertIn('control_flow', core.__all__)
    self.assertIn('sentinels', core.__all__)
    for name in ('ControlFlow', 'SkipSet', 'MetaFlow', 'ControlSpace'):
      self.assertIn(name, control_flow.__all__)
    self.assertTrue(issubclass(SkipSet, ControlFlow))
    self.assertIs(type(ControlFlow), MetaFlow)
    self.assertNotIn('ControlClassError', control_flow.__all__)

  def test_error_lives_in_meta(self) -> None:
    """'ControlClassError' is a class-body refusal and sits with its
    siblings."""
    self.assertIn('ControlClassError', waitaminute.meta.__all__)
    with self.assertRaises(ControlClassError):
      class Chatty(ControlFlow):
        tone = 'loud'

  def test_reexport_resolves_same_objects(self) -> None:
    """Every name the old package listed resolves to the moved object."""
    self.assertIs(reexport.ControlFlow, ControlFlow)
    self.assertIs(reexport.SkipSet, SkipSet)
    self.assertIs(reexport.MetaFlow, MetaFlow)
    self.assertIs(reexport.ControlSpace, ControlSpace)
    self.assertIs(reexport.ControlClassError, ControlClassError)
    expected = {
      'ControlClassError', 'ControlSpace', 'MetaFlow', 'ControlFlow',
      'SkipSet',
    }
    self.assertEqual(set(reexport.__all__), expected)

  def test_reexport_import_forms(self) -> None:
    """The 'from' import and the star import work through the
    re-export."""
    from worktoy.waitaminute.control_flow import SkipSet as viaShim
    self.assertIs(viaShim, SkipSet)
    space = dict()
    exec('from worktoy.waitaminute.control_flow import *', space)
    self.assertIs(space['ControlFlow'], ControlFlow)

  def test_reexport_refuses_unknown_name(self) -> None:
    """A name the family never had is refused as any module refuses
    one."""
    with self.assertRaises(AttributeError):
      _ = reexport.Halt
    with self.assertRaises(ImportError):
      exec('from worktoy.waitaminute.control_flow import Halt')

  def test_reexport_defines_nothing(self) -> None:
    """The re-export holds no class of its own, so a walk over the
    exceptions of 'waitaminute' finds the family once, in 'core'."""
    own = [
      name for name, value in vars(reexport).items()
      if isinstance(value, type) and value.__module__ == reexport.__name__
    ]
    self.assertEqual(own, [])
