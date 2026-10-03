"""
ReservedAttributeError is raised when an 'EZData' class body binds one of
the attributes 'EZData' keeps for itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from ...ezdata import EZSpace


class ReservedAttributeError(NoPickle, AttributeError):
  """
  ReservedAttributeError subclasses 'AttributeError' and is raised when an
  EZData class body binds one of the attributes EZData keeps for itself:
  '__ez_fields__', '__is_frozen__', '__is_ordered__', '__kw_only__' and
  '__ez_generated__', which EZData sets on every class, and
  '__key_args__', under which 'Object' keeps the keyword arguments of its
  constructor. Such a binding would become a field of that name, while
  EZData overwrote the class attribute with its own value:
  '__kw_only__ = True' in a class body would add a field named
  '__kw_only__' and leave the class positional. The options of an EZData
  class are set by class keyword, as in 'class Point(EZData,
  kwOnly=True)'. It is the attribute counterpart of 'ReservedMethodError'.

  Attributes
  ----------
  attributeName : str
    The reserved attribute name the class body bound.
  space : EZSpace
    The namespace under construction; carries the class name.
  """

  __slots__ = ('attributeName', 'space')

  def __init__(self, attributeName: str, space: EZSpace) -> None:
    self.attributeName = attributeName
    self.space = space
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """The class body of EZData class '%s' binds '%s', an
    attribute EZData keeps for itself. The options of an EZData class are
    set by class keyword, as in 'class %s(EZData, kwOnly=True)'."""
    clsName = self.space.getClassName()
    info = infoSpec % (clsName, self.attributeName, clsName)
    return textFmt(info)

  __repr__ = __str__
