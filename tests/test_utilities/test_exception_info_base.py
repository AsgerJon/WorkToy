"""
TestExceptionInfoBase subclasses 'UtilitiesTest' and pins that
'ExceptionInfo' refuses an expected exception it can never catch: a
'BaseException' that is not an 'Exception', such as 'KeyboardInterrupt',
always propagates from the block, so expecting one used to let the
interrupt through while the caller believed it would be caught.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import ExceptionInfo

from . import UtilitiesTest


class TestExceptionInfoBase(UtilitiesTest):
  """
  TestExceptionInfoBase provides tests for expecting a 'BaseException'
  that is not an 'Exception'.
  """

  def test_class_refused(self) -> None:
    """Such a class is refused with 'TypeError' naming it."""
    for excType in (KeyboardInterrupt, SystemExit, GeneratorExit):
      with self.subTest(excType=excType.__name__):
        with self.assertRaises(TypeError) as context:
          ExceptionInfo(excType)
        self.assertIn(excType.__name__, str(context.exception))

  def test_instance_refused(self) -> None:
    """An instance of such a class is refused as well."""
    with self.assertRaises(TypeError):
      ExceptionInfo(KeyboardInterrupt())

  def test_exception_accepted(self) -> None:
    """An 'Exception' is accepted and caught."""
    with ExceptionInfo(ValueError) as info:
      raise ValueError('caught')
    self.assertIs(info.actualExcType, ValueError)
