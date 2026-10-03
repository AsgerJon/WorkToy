"""
TestExceptionNameSlot subclasses 'EZTest' and pins that 'DuplicateError',
'ReservedFieldError' and 'ReservedMethodError' keep the name they report
under an attribute of their own. They kept it at 'name', which an
'AttributeError' reads as the attribute that was missing, so from Python
3.12 on, the traceback of a class body defining '__setattr__' ended with
"Did you mean: '__delattr__'?".
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import traceback

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import DuplicateError, ReservedFieldError
from worktoy.waitaminute.ezdata import ReservedMethodError

from . import EZTest


def _formatted(exception: BaseException) -> str:
  """The traceback of 'exception', as the interpreter prints it."""
  lines = traceback.format_exception(
    type(exception), exception, exception.__traceback__,
  )
  return ''.join(lines)


class TestExceptionNameSlot(EZTest):
  """
  TestExceptionNameSlot provides tests for the attribute holding the name
  each of the three exceptions reports.
  """

  def test_duplicate_field(self) -> None:
    """'DuplicateError' keeps the field name at 'fieldName'."""
    with self.assertRaises(DuplicateError) as context:
      class Twice(EZData):  # noqa: F841
        x = EZField[int](0)
        x = EZField[int](1)  # noqa: F811
    exception = context.exception
    self.assertEqual(exception.fieldName, 'x')
    self.assertIsNone(getattr(exception, 'name', None))
    self.assertNotIn('Did you mean', _formatted(exception))

  def test_reserved_field(self) -> None:
    """'ReservedFieldError' keeps the field name at 'fieldName'."""
    with self.assertRaises(ReservedFieldError) as context:
      class Taken(EZData):  # noqa: F841
        asDict = EZField[int](0)
    exception = context.exception
    self.assertEqual(exception.fieldName, 'asDict')
    self.assertIsNone(getattr(exception, 'name', None))
    self.assertNotIn('Did you mean', _formatted(exception))

  def test_reserved_method(self) -> None:
    """'ReservedMethodError' keeps the method name at 'methodName'."""
    with self.assertRaises(ReservedMethodError) as context:
      class Guarded(EZData):  # noqa: F841
        x = EZField[int](0)

        def __setattr__(self, key: str, value: object) -> None:
          """A method EZData keeps for itself."""
    exception = context.exception
    self.assertEqual(exception.methodName, '__setattr__')
    self.assertIsNone(getattr(exception, 'name', None))
    self.assertNotIn('Did you mean', _formatted(exception))
