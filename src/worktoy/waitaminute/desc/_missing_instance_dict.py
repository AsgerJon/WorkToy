"""
MissingInstanceDict is raised when a box must store a value on an instance
that has no instance dict.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class MissingInstanceDict(TypeError):
  """
  MissingInstanceDict is raised when a box, an 'AttriBox' or a class
  based on it, must store the value of its field on an instance that has
  no instance dict, as an instance of a class declaring '__slots__'
  without '__dict__' has none. The store used to fail with the bare
  'AttributeError' of 'object.__setattr__', which the attribute protocol
  reads as the attribute being absent, so 'hasattr' answered 'False' and
  nothing said the box could not work there. It subclasses 'TypeError',
  since the owner is of a kind the box cannot serve.

  Attributes
  ----------
  instance : Any
    The instance the box could not store on.
  ownerName : str
    The name of the class of that instance.
  fieldName : str
    The name of the field.
  """

  __slots__ = ('instance', 'ownerName', 'fieldName')

  def __init__(self, instance: Any, fieldName: str) -> None:
    self.instance = instance
    self.ownerName = type(instance).__name__
    self.fieldName = fieldName
    TypeError.__init__(self, )

  def __str__(self) -> str:
    spec = """The box at '%s.%s' stores the value of its field in the
    instance dict, but instances of '%s' have no '__dict__': the class
    declares '__slots__' without one. Add '__dict__' to the slots, or
    hold the value in a slot of the class."""
    names = (self.ownerName, self.fieldName, self.ownerName)
    return textFmt(spec % names)

  __repr__ = __str__
