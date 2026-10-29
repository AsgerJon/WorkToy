"""
SharedDescriptor is raised when a descriptor already placed on a class is
placed again.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class SharedDescriptor(WorkToyException, SyntaxError):
  """
  SharedDescriptor is raised when a descriptor based on 'BaseDescriptor',
  such as an 'AttriBox' or a 'Field', is placed when it is already placed
  on a class, as when one box object is bound in the bodies of two
  classes:

    shared = AttriBox[Point]()

    class A(BaseObject):
      p = shared

    class B(BaseObject):
      p = shared    # SharedDescriptor

  A descriptor records the class and the name it is placed at as the
  class is created, and a box names that class in the tags of the values
  it builds, so one descriptor cannot serve two places. The second
  placement used to take the first over, and the values built for the
  instances of 'A' named 'B' as their owner. A field meant for several
  classes is declared in a common base, or each class takes a
  descriptor of its own, for instance from a function returning a new
  one. A descriptor bound to two names in one class body, as in
  'width = height = AttriBox[int](0)', is not refused:
  'BaseDescriptor.__set_name__' places a clone of it at the second name.
  It subclasses 'SyntaxError', as the other refusals of a class-body line
  do.

  Attributes
  ----------
  desc : Any
    The descriptor placed again.
  owner : type
    The class the descriptor was placed on first.
  fieldName : str
    The name the descriptor was placed at first.
  newOwner : type
    The class placing it again.
  newName : str
    The name it is placed at again.
  """

  __slots__ = ('desc', 'owner', 'fieldName', 'newOwner', 'newName',)

  def __init__(
      self,
      desc: Any,
      owner: type,
      fieldName: str,
      newOwner: type,
      newName: str,
  ) -> None:
    self.desc = desc
    self.owner = owner
    self.fieldName = fieldName
    self.newOwner = newOwner
    self.newName = newName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The '%s' at '%s.%s' is placed again at '%s.%s'. A descriptor
    belongs to the one class it is placed on: declare the field in a base
    of both classes, or give each class a descriptor of its own."""
    names = (
      type(self.desc).__name__,
      self.owner.__name__, self.fieldName,
      self.newOwner.__name__, self.newName,
    )
    return textFmt(spec % names)

  __repr__ = __str__
