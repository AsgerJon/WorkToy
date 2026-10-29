"""
TestWorkToyException subclasses 'WaitAMinuteTest' and pins that every
exception of 'worktoy.waitaminute', the control-flow signals aside, is a
'WorkToyException' and keeps the builtin it is based on, so one 'except
WorkToyException' catches every exception of the library and the
builtin's own 'except' clauses keep working.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pkgutil
import importlib

from worktoy import waitaminute
from worktoy.waitaminute import WorkToyException, TypeException
from worktoy.core.control_flow import ControlFlow, SkipSet
from worktoy.waitaminute.desc import ReadOnlyError, DescriptorException
from worktoy.waitaminute.meta import ClaimedName

from . import WaitAMinuteTest


def _exceptionClasses() -> list:
  """Every exception class defined in a module of 'worktoy.waitaminute'
  outside the control-flow package."""
  out = []
  prefix = waitaminute.__name__ + '.'
  for info in pkgutil.walk_packages(waitaminute.__path__, prefix):
    if '.control_flow' in info.name:
      continue
    module = importlib.import_module(info.name)
    for value in vars(module).values():
      if not isinstance(value, type):
        continue
      if not issubclass(value, BaseException):
        continue
      if value.__module__ != module.__name__:
        continue
      if value not in out:
        out.append(value)
  return out


class TestWorkToyException(WaitAMinuteTest):
  """
  TestWorkToyException provides tests for the common exception base.
  """

  def test_every_exception_joins(self) -> None:
    """Every exception of the package, the control-flow signals aside,
    is a 'WorkToyException' and keeps the builtin it is based on."""
    classes = _exceptionClasses()
    self.assertGreater(len(classes), 40)
    for cls in classes:
      with self.subTest(cls=cls.__name__):
        self.assertTrue(issubclass(cls, WorkToyException))
        self.assertTrue(issubclass(cls, Exception))
    self.assertFalse(issubclass(ControlFlow, WorkToyException))
    self.assertFalse(issubclass(SkipSet, WorkToyException))
    self.assertTrue(issubclass(DescriptorException, WorkToyException))

  def test_caught_by_builtin_and_by_base(self) -> None:
    """An exception is caught by the builtin it is based on and by the
    common base alike, whatever the builtin."""
    with self.assertRaises(TypeError):
      raise TypeException('n', 1, int)
    with self.assertRaises(WorkToyException):
      raise TypeException('n', 1, int)
    with self.assertRaises(AttributeError):
      raise ReadOnlyError(3, 'desc', 4)
    with self.assertRaises(SyntaxError):
      raise ClaimedName('Foo', 'x')
    with self.assertRaises(WorkToyException):
      raise ClaimedName('Foo', 'x')

  def test_base_adds_no_layout(self) -> None:
    """The common base declares empty slots, so it stands beside
    'SyntaxError', whose layout is wider than that of 'Exception', and a
    refusal based on it keeps 'msg' for the traceback."""
    self.assertEqual(WorkToyException.__slots__, ())
    refusal = ClaimedName('Foo', 'x')
    self.assertIsInstance(refusal, SyntaxError)
    self.assertEqual(refusal.msg, str(refusal))
