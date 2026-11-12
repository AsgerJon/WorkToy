"""
TestWaitaminutePackage tests the public face of 'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import ModuleType

from worktoy import waitaminute
from worktoy.waitaminute import WorkToyException, WorkToyWarning
from . import WaitaminuteTest


class TestWaitaminutePackage(WaitaminuteTest):
  """
  The package exports the common base, six cross-cutting exceptions,
  the common base of the warnings with the four warnings, and six
  subpackages, one per layer that raises. Every exported warning lists
  'WorkToyWarning' first and the builtin category it keeps second, as
  the exceptions do with theirs. Every exported exception
  lists 'WorkToyException' first and the builtin it keeps second, so
  one 'except WorkToyException' catches every exception of the library
  while an existing 'except TypeError' still catches the ones that are
  'TypeError's. The tests pin the exports and that layering.
  """

  def test_exports(self) -> None:
    expected = [
      'WorkToyException', 'TypeException', 'UncheckableType',
      'VariableNotNone', 'UnpackException', 'SubclassException',
      'MissingVariable', 'WorkToyWarning', 'DeprecatedPromise',
      'RiskWarning', 'AlternativeWarning', 'RedundantKeyword', 'desc',
      'meta', 'dispatch', 'keenum', 'ezdata', 'control_flow',
    ]
    self.assertEqual(waitaminute.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(waitaminute, name))

  def test_common_base(self) -> None:
    self.assertEqual(WorkToyException.__bases__, (Exception,))
    self.assertEqual(WorkToyException.__slots__, ())
    builtins = {
      'TypeException': TypeError, 'UncheckableType': TypeError,
      'VariableNotNone': Exception, 'UnpackException': ValueError,
      'SubclassException': TypeError, 'MissingVariable': AttributeError,
    }
    for name, builtin in builtins.items():
      with self.subTest(name=name):
        cls = getattr(waitaminute, name)
        self.assertEqual(cls.__bases__, (WorkToyException, builtin))
        self.assertIsInstance(cls.__slots__, tuple)

  def test_warnings(self) -> None:
    self.assertEqual(WorkToyWarning.__bases__, (Warning,))
    self.assertEqual(WorkToyWarning.__slots__, ())
    builtins = {
      'DeprecatedPromise': FutureWarning, 'RiskWarning': RuntimeWarning,
      'AlternativeWarning': UserWarning,
      'RedundantKeyword': UserWarning,
    }
    for name, builtin in builtins.items():
      with self.subTest(name=name):
        cls = getattr(waitaminute, name)
        self.assertEqual(cls.__bases__, (WorkToyWarning, builtin))
        self.assertIsInstance(cls.__slots__, tuple)

  def test_subpackages(self) -> None:
    for name in ('desc', 'meta', 'dispatch', 'keenum', 'ezdata'):
      with self.subTest(name=name):
        package = getattr(waitaminute, name)
        self.assertIsInstance(package, ModuleType)
        for exported in package.__all__:
          self.assertIsSubclass(getattr(package, exported),
                                WorkToyException)
    self.assertIsInstance(waitaminute.control_flow, ModuleType)
