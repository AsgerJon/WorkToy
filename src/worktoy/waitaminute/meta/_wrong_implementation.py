"""
WrongImplementation is raised when a class body writes a method that
cannot take what the abstract method it implements declares.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class WrongImplementation(WorkToyException, SyntaxError):
  """
  A class based on an abstract class may leave an abstract method
  unwritten, for a further subclass to write, and stays abstract while
  it does. A method it does write has to be right: the same kind of
  method as the one declared, and able to receive everything that one
  declares. One that is not would answer some calls the declaration
  allows with Python's own complaint about arguments, far from the
  class that made the mistake, so the mistake fails where it is made.

  Implementation
  --------------

  The namespace of a class built by 'ABCMeta' raises it at the line of
  the class body that writes the method, or as the class is created
  where only the whole body shows the mistake. The blank function of an
  abstract declaration is held to each signature stacked on it the same
  way. It subclasses 'SyntaxError', as the other refusals of a
  class-body line do.

  Attributes
  ----------

  className : str
    The name of the class under construction.

  name : str
    What is written wrongly: the name of a method declared plainly, and
    the name with the signature for an abstract overload.

  declared : str
    What the abstract method declares, in words.

  written : str
    What the class body wrote, in words.
  """

  __slots__ = ('className', 'name', 'declared', 'written')

  def __init__(
      self,
      className: str,
      name: str,
      declared: str,
      written: str,
  ) -> None:
    self.className = className
    self.name = name
    self.declared = declared
    self.written = written
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self, ) -> str:
    infoSpec = """The class body of '%s' writes '%s' wrongly: it is
    declared as %s, and written as %s."""
    info = infoSpec % (
      self.className, self.name, self.declared, self.written,
    )
    return textFmt(info)

  __repr__ = __str__
