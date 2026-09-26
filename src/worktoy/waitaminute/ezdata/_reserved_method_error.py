"""
ReservedMethodError is raised when an 'EZData' class body defines a
method that 'EZData' generates and does not allow to be replaced.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from ...ezdata import EZSpace


class ReservedMethodError(AttributeError):
  """
  ReservedMethodError subclasses 'AttributeError' and is raised when an
  EZData class body defines a method that EZData generates for every
  class and keeps for itself. The method '__setattr__' is one: the
  generated version casts each assignment to the field type, or refuses
  it on a frozen class, and a replacement could break the guarantee that
  every field holds a value of its declared type. Validation and derived
  state belong in '__post_init__' instead.

  Attributes
  ----------
  name : str
    The reserved method name the class body defined.
  space : EZSpace
    The namespace under construction; carries the class name and the
    reserved-method list.
  """

  __slots__ = ('name', 'space')

  def __init__(self, name: str, space: EZSpace) -> None:
    self.name = name
    self.space = space
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The class body of EZData class '%s' defines '%s', which
    EZData generates itself and does not allow to be replaced. Use
    '__post_init__' for validation and derived state."""
    info = infoSpec % (self.space.getClassName(), self.name)
    return textFmt(info)

  __repr__ = __str__
