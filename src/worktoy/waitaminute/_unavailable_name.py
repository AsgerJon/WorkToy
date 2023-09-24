"""WorkSide - Wait A Minute! - UnavailableName
Exception raised when a name is already occupied."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class UnavailableNameException(MetaXcept):
  """WorkSide - Wait A Minute! - UnavailableName
  Exception raised when a name is already occupied."""

  def __init__(self, name: str, oldVal: Any, newVal: Any = None,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._name = name
    self._oldVal = oldVal
    self._newVal = newVal

  def __full_str__(self) -> str:
    """Message issued when receiving the new value."""
    header = MetaXcept.__str__(self)
    newVal = self._newVal
    name = self._name
    oldVal = self._oldVal
    msg = """Attempted to overwrite variable named '%s'. This name was 
    expected to refer to a variable valued 'None', but found value '%s'. 
    The attempted new value was '%s'."""
    body = msg % (newVal, name, oldVal)
    return '%s\n%s' % (header, self.justify(body))

  def __str__(self, ) -> str:
    if self._newVal is not None:
      return self.__full_str__()
    return self.__name_val_str__()
