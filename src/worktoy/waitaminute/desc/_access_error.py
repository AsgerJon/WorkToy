"""
AccessError is raised when a descriptor has no way to retrieve a value.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescriptorException
from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class AccessError(DescriptorException, AttributeError):
  """
  AccessError is raised when a descriptor has no way to retrieve a value,
  for example a 'Field' whose getter was never registered with '@x.GET'.
  It subclasses both 'DescriptorException' and 'AttributeError', so it is
  caught by either.

  Attributes
  ----------
  desc : object
    The descriptor that could not produce a value.
  """

  __slots__ = ('desc',)

  def __init__(self, desc) -> None:
    self.desc = desc
    DescriptorException.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The '%s' descriptor at '%s.%s' failed to retrieve a 
    value!"""
    descTypeName = type(self.desc).__name__
    ownerName = self.desc.__field_owner__.__name__
    fieldName = self.desc.__field_name__
    info = infoSpec % (descTypeName, ownerName, fieldName)
    return textFmt(info)

  __repr__ = __str__
