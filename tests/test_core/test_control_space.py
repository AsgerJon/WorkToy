"""
TestControlSpace tests 'ControlSpace' from 'worktoy.core.control_flow'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.control_flow import ControlSpace, MetaFlow, ControlFlow
from worktoy.waitaminute.meta import ControlClassError
from . import CoreTest


class TestControlSpace(CoreTest):
  """
  A signal is used by its type alone, so a signal body defining methods
  or state is a mistake that should fail at the line making it.
  'ControlSpace' is the namespace of a signal body: it admits the names
  on its white list and the data attributes 'Exception' holds, and
  refuses the rest with 'ControlClassError', except in the body of the
  root. The tests pin each of these.
  """

  def test_white_list(self) -> None:
    names = ControlSpace._getWhiteList()
    self.assertEqual(names, ControlSpace.__white_list__)
    for name in ('__str__', '__repr__', '__classcell__', '__classdictcell__',
                 '__firstlineno__', '__static_attributes__'):
      with self.subTest(name=name):
        self.assertIn(name, names)

  def test_init_records_statement(self) -> None:
    space = ControlSpace(MetaFlow, 'Sig', (ControlFlow,))
    self.assertIs(space.__metaclass__, MetaFlow)
    self.assertEqual(space.__base_classes__, (ControlFlow,))
    self.assertEqual(space.__class_name__, 'Sig')
    self.assertIs(space.__is_root__, False)
    self.assertEqual(space, {})
    root = ControlSpace(MetaFlow, 'Root', (), _root=True)
    self.assertIs(root.__is_root__, True)

  def test_white_listed_names_admitted(self) -> None:
    space = ControlSpace(MetaFlow, 'Sig', (ControlFlow,))
    for name in ControlSpace._getWhiteList():
      space[name] = name
    self.assertEqual(len(space), len(ControlSpace._getWhiteList()))

  def test_data_names_of_exception_admitted(self) -> None:
    space = ControlSpace(MetaFlow, 'Sig', (ControlFlow,))
    for name in ('__module__', '__qualname__', '__doc__'):
      with self.subTest(name=name):
        space[name] = name
        self.assertEqual(space[name], name)

  def test_other_names_refused(self) -> None:
    space = ControlSpace(MetaFlow, 'Sig', (ControlFlow,))
    #  'args' is the one plain name 'Exception' holds as data: bound in
    #  a signal body it would be state the signal carries.
    names = ('method', 'value', '__init__', 'with_traceback', '__slots__',
             'args')
    for name in names:
      with self.subTest(name=name):
        with self.assertRaises(ControlClassError) as context:
          space[name] = 1
        self.assertIs(context.exception.space, space)
        self.assertEqual(context.exception.badKey, name)
        self.assertIsInstance(context.exception, TypeError)
        self.assertIn("'Sig'", str(context.exception))
        self.assertIn("binds '%s'" % name, str(context.exception))
    self.assertEqual(space, {})

  def test_root_body_unchecked(self) -> None:
    space = ControlSpace(MetaFlow, 'Root', (), _root=True)
    space['anything'] = 1
    space['with_traceback'] = 2
    self.assertEqual(space, {'anything': 1, 'with_traceback': 2})

  def test_unset_root_flag_reads_as_not_root(self) -> None:
    space = ControlSpace.__new__(ControlSpace)
    self.assertIsNone(space.__is_root__)
    with self.assertRaises(ControlClassError) as context:
      space['anything'] = 1
    self.assertIs(context.exception.space, space)
    self.assertEqual(context.exception.badKey, 'anything')
    #  A space built without a metaclass has no root to name, so the
    #  message of this one cannot render; its slots are the record.
    space['__str__'] = 1
    self.assertEqual(space, {'__str__': 1})
