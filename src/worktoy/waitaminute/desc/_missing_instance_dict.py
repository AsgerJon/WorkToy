"""
MissingInstanceDict is raised when a box must store a value on an instance
that has no instance dict.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class MissingInstanceDict(WorkToyException, TypeError):
  """
  MissingInstanceDict is raised when a box, an 'AttriBox', a class based
  on it or a 'FastBox', is placed on a class whose instances have no
  instance dict, as instances of a class declaring '__slots__' without
  '__dict__' have none. The box refuses such a class as it is created, in
  '__set_name__', and refuses an access the same way should it be
  installed on one with 'setattr' afterwards. The store used to fail with
  the bare 'AttributeError' of 'object.__setattr__', which the attribute
  protocol reads as the attribute being absent, so 'hasattr' answered
  'False' and nothing said the box could not work there. It subclasses
  'TypeError', since the owner is of a kind the box cannot serve.

  Attributes
  ----------
  instance : Any
    The owner class, when the box is refused as the class is created, or
    the instance the box could not store on.
  ownerName : str
    The name of that class, or of the class of that instance.
  fieldName : str
    The name of the field.
  """

  __slots__ = ('instance', 'ownerName', 'fieldName')

  def __init__(self, instance: Any, fieldName: str) -> None:
    self.instance = instance
    owner = instance if isinstance(instance, type) else type(instance)
    self.ownerName = owner.__name__
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
