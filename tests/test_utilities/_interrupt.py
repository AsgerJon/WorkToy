"""
Interrupt is a 'BaseException' that is no 'Exception', raised by the
tests of 'ExceptionInfo' in place of 'KeyboardInterrupt'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class Interrupt(BaseException):
  """
  A test of what 'ExceptionInfo' does with a 'BaseException' that is no
  'Exception' cannot raise 'KeyboardInterrupt' or 'SystemExit', which
  the test runner itself acts on. 'Interrupt' is such an exception that
  nothing but the test cares about.
  """
  pass
