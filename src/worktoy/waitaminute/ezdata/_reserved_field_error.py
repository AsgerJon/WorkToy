"""
ReservedFieldError is raised when an EZData class body attempts to
declare an EZField at a name that the EZData machinery reserves
for its generated conversion helpers and display dunders, such as
'asDict', 'asTuple', or 'replace'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from ...ezdata import EZSpace


class ReservedFieldError(AttributeError):
  """
  ReservedFieldError subclasses 'AttributeError' and is raised
  when an EZData class body declares an EZField at a name that
  EZData reserves for one of its generated methods. Method
  overrides at these names remain allowed; only EZField
  declarations are rejected.

  Attributes
  ----------
  name : str
    The reserved name the user attempted to bind an EZField to.
  space : EZSpace
    The namespace under construction; carries the class name and
    the reserved-name list.
  """

  __slots__ = ('name', 'space')

  def __init__(self, name: str, space: EZSpace) -> None:
    self.name = name
    self.space = space
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = (
      "In the class body of EZData class '%s', the name '%s' is "
      "reserved for a generated method and cannot be used as a "
      "field name. Reserved names: %s. Method overrides at these "
      "names are allowed; only EZField declarations are rejected."
    )
    clsName = self.space.getClassName()
    reserved = ', '.join(
      repr(n) for n in self.space.__reserved_ez_names__
    )
    return infoSpec % (clsName, self.name, reserved)

  __repr__ = __str__
