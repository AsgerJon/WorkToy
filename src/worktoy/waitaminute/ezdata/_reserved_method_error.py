"""
ReservedMethodError is raised when an 'EZData' class body defines a
method that 'EZData' generates and does not allow to be replaced.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from ...ezdata import EZSpace


class ReservedMethodError(NoPickle, AttributeError):
  """
  ReservedMethodError subclasses 'AttributeError' and is raised when an
  EZData class body defines a method that EZData generates for every
  class and keeps for itself: '__init__', '__iter__', '__len__',
  '__eq__', '__hash__', the four ordering methods, '__setattr__' and
  '__delattr__'. EZData installs these after the class body, so a
  class-body definition would be dropped without a word; the
  construction, the assignment and the deletion guard the rule that
  every field holds a value of its declared type, iteration and length
  both run over the fields, and equality, hashing and ordering all
  compare the field values. Validation and derived state belong in
  '__post_init__' instead. A plain base, one not built by 'EZMeta', may
  define these methods, as a mixin written against the same protocol
  does; the generated methods take precedence over them.

  Attributes
  ----------
  methodName : str
    The reserved method name the class body defined. It is not kept at
    'name', which an 'AttributeError' reads as the name of a missing
    attribute, and which tracebacks from Python 3.12 on answer with a
    suggestion.
  space : EZSpace
    The namespace under construction; carries the class name and the
    reserved-method list.
  """

  __slots__ = ('methodName', 'space')

  def __init__(self, methodName: str, space: EZSpace) -> None:
    self.methodName = methodName
    self.space = space
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The class body of EZData class '%s' defines '%s', which
    EZData generates itself and does not allow to be replaced. Use
    '__post_init__' for validation and derived state."""
    info = infoSpec % (self.space.getClassName(), self.methodName)
    return textFmt(info)

  __repr__ = __str__
