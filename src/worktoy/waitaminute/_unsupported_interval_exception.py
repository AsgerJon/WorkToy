"""WorkToy - Wait A Minute! - UnsupportedIntervalException
Exception raised when a variable has a value of the correct type,
but outside the supported interval."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class UnsupportedIntervalException(MetaXcept):
  """WorkToy - Wait A Minute! - UnsupportedIntervalException
  Exception raised when a variable has a value of the correct type,
  but outside the supported interval."""

  def __init__(self, value: Any,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._value = self.pretty(value)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    msg = """Given value: %s is not in supported interval!"""
    body = msg % self._value
    return '%s\n%s' % (header, self.justify(body))
