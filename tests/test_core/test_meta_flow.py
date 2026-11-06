"""
TestMetaFlow tests 'MetaFlow' from 'worktoy.core.control_flow'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.core.control_flow import MetaFlow, ControlSpace, ControlFlow
from worktoy.core.control_flow import SkipSet
from worktoy.core._meta_type import _Chill
from worktoy.waitaminute import VariableNotNone
from . import CoreTest


class TestMetaFlow(CoreTest):
  """
  'MetaFlow' builds the control-flow signals: it prepares a
  'ControlSpace' holding the text functions and the root flag, keeps
  the one root, and gives each signal class and instance a text naming
  the signal. The tests pin the root, the refusal of a second root, the
  prepared namespace, the texts, and that a signal is a 'MetaType'
  class like every other.
  """

  def test_root(self) -> None:
    self.assertIs(MetaFlow.getRootClass(), ControlFlow)
    self.assertIs(ControlFlow.__is_root__, True)
    self.assertIs(SkipSet.__is_root__, False)

  def test_second_root_refused(self) -> None:
    with self.assertRaises(VariableNotNone) as context:
      class CORE_ROOT(Exception, metaclass=MetaFlow, _root=True):
        pass
    self.assertEqual(context.exception.name, '__root_cls__')
    self.assertIs(context.exception.value, ControlFlow)
    self.assertIn('__root_cls__', str(context.exception))
    self.assertIn('ControlFlow', str(context.exception))
    self.assertIs(MetaFlow.getRootClass(), ControlFlow)

  def test_prepare(self) -> None:
    space = MetaFlow.__prepare__('Sig', (ControlFlow,))
    self.assertIsInstance(space, ControlSpace)
    self.assertIs(space['__str__'], space['__repr__'])
    self.assertIs(space['__is_root__'], False)
    self.assertEqual(space['__str__'](SkipSet()), '<ControlFlow: SkipSet>')
    root = MetaFlow.__prepare__('Root', (), _root=True)
    self.assertIs(root['__is_root__'], True)
    self.assertIs(root.__is_root__, True)

  def test_text(self) -> None:
    self.assertEqual(str(ControlFlow), '<ControlFlow: [Root]>')
    self.assertEqual(repr(ControlFlow), '<ControlFlow: [Root]>')
    self.assertEqual(str(SkipSet), '<ControlFlow: SkipSet>')
    self.assertEqual(repr(SkipSet), '<ControlFlow: SkipSet>')
    self.assertEqual(str(SkipSet()), '<ControlFlow: SkipSet>')
    self.assertEqual(repr(SkipSet('ignored')), '<ControlFlow: SkipSet>')
    self.assertEqual(str(ControlFlow()), '<ControlFlow: [Root]>')

  def test_str_factory(self) -> None:
    text = MetaFlow._strFactory()
    self.assertEqual(text(SkipSet()), str(SkipSet))
    self.assertEqual(SkipSet._strFactory()(SkipSet()), str(SkipSet))
    self.assertEqual(text(ControlFlow()), '<ControlFlow: [Root]>')

  def test_signal_is_a_worktoy_class(self) -> None:
    self.assertIsInstance(SkipSet, MetaFlow)
    self.assertIsInstance(MetaFlow, MetaType)
    self.assertIsInstance(SkipSet.__namespace__, ControlSpace)
    self.assertEqual(SkipSet.__mro__.count(_Chill), 1)
    self.assertFalse(SkipSet.__skip_hash__)
