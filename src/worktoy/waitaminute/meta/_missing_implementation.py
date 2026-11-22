"""
MissingImplementation is raised when a class is instantiated while a
method it declares abstract is not implemented.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from . import IllegalInstantiation


class MissingImplementation(IllegalInstantiation):
  """
  A class built by 'ABCMeta' may declare methods with '@abstract', which
  the classes based on it have to write. Until each is written the class
  is abstract, and an object of it would answer some of its methods with
  nothing. Whoever tries to make one must be told which methods are
  left, since that is the list of what a subclass still has to write.

  Implementation
  --------------

  'ABCMeta' raises it when an abstract class is called, before '__new__'
  and '__init__' run. It subclasses 'IllegalInstantiation', so it is a
  'TypeError', and code catching that exception for a class that may not
  be instantiated catches this one as well. Raised by hand without a
  name, it reads as 'IllegalInstantiation' does.

  Attributes
  ----------

  cls : type
    The abstract class, kept by 'IllegalInstantiation'.

  names : tuple[str, ...]
    What is not implemented: the name of a method declared plainly, and
    the name with the signature for an abstract overload, as
    'data(str, int)'; a classmethod or staticmethod is named as such.
  """

  __slots__ = ('names',)

  def __init__(self, cls_: type, *names) -> None:
    self.names = names
    IllegalInstantiation.__init__(self, cls_)

  def __str__(self, ) -> str:
    if not self.names:
      #  This branch is reached by the following:
      #  - The exception is raised by hand without a name; 'ABCMeta'
      #    raises it only for a class that lacks something
      return IllegalInstantiation.__str__(self)
    quoted = ', '.join("'%s'" % name for name in self.names)
    if len(self.names) == 1:
      infoSpec = """The class '%s' cannot be instantiated: %s is declared
      abstract and not implemented."""
    else:
      infoSpec = """The class '%s' cannot be instantiated: %s are declared
      abstract and not implemented."""
    return textFmt(infoSpec % (self.cls.__name__, quoted))

  __repr__ = __str__
