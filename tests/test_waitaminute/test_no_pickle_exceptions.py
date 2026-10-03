"""
TestNoPickleExceptions subclasses 'WaitAMinuteTest' from the
'tests.test_waitaminute' package and pins that every exception exported by
'worktoy.waitaminute' and its packages refuses to be pickled, by any
protocol, with 'PickleException'. The instances are made by '__new__'
alone, so the sweep reaches each exception without knowing its
constructor.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle

from worktoy import waitaminute
from worktoy.waitaminute import PickleException

from . import WaitAMinuteTest

_PACKAGES = (
  waitaminute,
  waitaminute.desc,
  waitaminute.meta,
  waitaminute.dispatch,
  waitaminute.keenum,
  waitaminute.ezdata,
  waitaminute.control_flow,
)


def _exceptionClasses() -> list[type]:
  """The exception classes the 'waitaminute' packages export."""
  out = []
  for package in _PACKAGES:
    for name in package.__all__:
      obj = getattr(package, name)
      if isinstance(obj, type) and issubclass(obj, BaseException):
        out.append(obj)
  return out


class TestNoPickleExceptions(WaitAMinuteTest):
  """
  TestNoPickleExceptions provides tests for the refusal to pickle every
  exception of 'worktoy'.
  """

  def test_sweep_finds_the_exceptions(self) -> None:
    """The sweep reaches every exported exception, 'PickleException'
    included."""
    classes = _exceptionClasses()
    self.assertGreaterEqual(len(classes), 44)
    self.assertIn(PickleException, classes)

  def test_every_exception_refuses(self) -> None:
    """Every exported exception raises 'PickleException' when pickled."""
    for cls in _exceptionClasses():
      exception = cls.__new__(cls)
      for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        with self.subTest(exception=cls.__name__, protocol=protocol):
          with self.assertRaises(PickleException):
            pickle.dumps(exception, protocol)
