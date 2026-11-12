"""
KeeTypeException is raised when the value of a member of an enumeration
is not an instance of the value type the enumeration established.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class KeeTypeException(WorkToyException, TypeError):
  """
  Raised when the value of a member is not an instance of the value type
  its enumeration established. A 'KeeNum' takes its value type from its
  first member, and every member must share it. A 'KeeFlags' class takes
  its value type from its first flag, and no combination may contain a
  member whose value is not an instance of it; since every flag is the
  combination of itself, that holds every flag to the type, while the
  value of a combination itself is free, and 'NULL', containing no
  member, cannot break the rule.

  Attributes
  ----------
  name : str
    The name of the member whose value had the wrong type.
  value : Any
    The value that was rejected.
  expectedTypes : tuple of type
    The accepted type(s) for member values.
  """

  __slots__ = ('name', 'value', 'expectedTypes')

  def __init__(self, name: str, value: Any, *types) -> None:
    self.name = name
    self.value = value
    self.expectedTypes = types
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Member '%s' has value %s of type '%s', but expected
    the value to be an instance of %s!"""
    name = self.name
    typeNames = [getattr(t, '__name__', str(t)) for t in self.expectedTypes]
    from ...utilities import joinWords, textFmt
    typeStr = joinWords(*["""'%s'""" % n for n in typeNames], sep='or')
    value = self._reprOf(self.value)
    valueType = type(self.value).__name__
    info = infoSpec % (name, value, valueType, typeStr)
    return textFmt(info)

  __repr__ = __str__
