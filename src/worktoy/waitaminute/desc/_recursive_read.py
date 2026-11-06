"""
RecursiveRead is raised when a field is read again while its own read
notification for the same instance is still running.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class RecursiveRead(WorkToyException, RecursionError):
  """
  RecursiveRead is raised when a field is read while its own 'preGet' or
  'onGet' notification for the same instance is still running. Such a
  read would run the notification again, which would read the field
  again, and so on until Python gave up with a bare 'RecursionError' a
  thousand frames later; the same happens when the callbacks of two
  instances read each other's field. The read is refused at the line
  making it instead. A read of another instance, or of another field, is
  no repeat, and a read made by the getter of the field itself, outside
  the notifications, is not refused. It subclasses 'RecursionError', so
  code catching that catches it as well.

  Attributes
  ----------
  desc : Any
    The descriptor read again.
  instance : Any
    The instance it was read through.
  phase : str
    The notification that was running, 'preGet' or 'onGet'.
  """

  __slots__ = ('desc', 'instance', 'phase')

  def __init__(self, desc: Any, instance: Any, phase: str) -> None:
    self.desc = desc
    self.instance = instance
    self.phase = phase
    RecursionError.__init__(self, )

  def __str__(self) -> str:
    spec = """'%s.%s' was read while its own '%s' notification for the
    same instance was still running, so the notification would start
    again and never end."""
    fieldId = (type(self.instance).__name__, self.desc.getFieldName())
    info = spec % (*fieldId, self.phase)
    if self.phase == 'onGet':
      hint = """The value being read is the second argument of the 'onGet'
      callback."""
    else:
      hint = """A 'preGet' callback runs before the value is read; an
      'onGet' callback receives it as its second argument."""
    return textFmt(info, hint)

  __repr__ = __str__
