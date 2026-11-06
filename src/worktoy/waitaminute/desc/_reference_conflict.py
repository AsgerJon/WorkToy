"""
ReferenceConflict is raised when a class body declares a name itself and
also decorates the inherited descriptor of that name through 'THIS'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class ReferenceConflict(WorkToyException, SyntaxError):
  """
  ReferenceConflict is raised when a class body declares a name itself
  and also decorates the descriptor of that name it inherits, through a
  reference such as 'THIS[Parent].x'. The reference stands for 'x' as the
  subclass will hold it, a clone of the inherited descriptor placed on
  the subclass as it is created, so it would replace the body's own 'x',
  and the declaration would be lost without a word. A body decorates a
  descriptor of its own directly, as in '@x.onSet'. The refusal comes as
  the class is created, from the '__init_subclass__' that 'THIS' installs,
  so no 'RuntimeError' wraps it on any version. It subclasses
  'SyntaxError', as the other refusals of a class-body line do.

  Attributes
  ----------
  className : str
    The name of the class whose body declares the name.
  fieldName : str
    The name both declared and reached through 'THIS'.
  holderName : str
    The name of the class holding the inherited descriptor.
  """

  __slots__ = ('className', 'fieldName', 'holderName')

  def __init__(
      self,
      className: str,
      fieldName: str,
      holderName: str,
  ) -> None:
    self.className = className
    self.fieldName = fieldName
    self.holderName = holderName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class body of '%s' declares '%s' itself and also
    decorates 'THIS[%s].%s', which stands for the '%s' it inherits. The
    reference would replace the declaration with a clone of the inherited
    descriptor."""
    rule = """A class body decorates a descriptor of its own directly, as
    in '@%s.onSet'."""
    names = (
      self.className, self.fieldName, self.holderName, self.fieldName,
      self.fieldName,
    )
    return textFmt(spec % names, rule % self.fieldName)

  __repr__ = __str__
