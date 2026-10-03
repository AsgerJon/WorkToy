"""
ClassFieldError is raised when an 'EZData' class body binds a name to a
class object.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class ClassFieldError(NoPickle, TypeError):
  """
  ClassFieldError is raised at class construction time when an 'EZData'
  class body binds a name to a class object, either through a nested
  class statement or through an assignment such as 'kind = int'. A bare
  class-body value becomes a field of the type of the value, so a class
  would become a field of type 'type' with the class as its default, and
  a nested class statement would quietly add a field to the constructor,
  the equality and the conversions. The class body fails at the
  offending line instead.

  Attributes
  ----------
  clsName : str
    The name of the EZData subclass under construction.
  fieldName : str
    The name the class object was bound to in the class body.
  classObject : type
    The class object that was bound.
  """

  __slots__ = ('clsName', 'fieldName', 'classObject')

  def __init__(
      self,
      clsName: str,
      fieldName: str,
      classObject: type,
  ) -> None:
    self.clsName = clsName
    self.fieldName = fieldName
    self.classObject = classObject
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData subclass '%s' binds the name '%s' to the class
    '%s'. A class object cannot become a field, so bind it outside the
    class body."""
    className = self.classObject.__name__
    info = infoSpec % (self.clsName, self.fieldName, className)
    return textFmt(info)

  __repr__ = __str__
