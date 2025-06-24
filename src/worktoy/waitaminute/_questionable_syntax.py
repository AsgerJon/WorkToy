"""QuestionableSyntax is raised when a name is encountered that is likely
a typo, such as '__set_item__' instead of '__setitem__' or '__setname__'
instead of '__set_name__'.
This is a"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Self


class QuestionableSyntax(SyntaxError):
  """QuestionableSyntax is raised when a name is encountered that is likely
  a typo, such as '__set_item__' instead of '__setitem__' or '__setname__'
  instead of '__set_name__'.
  This is a subclass of SyntaxError and should be used to indicate that
  the code is likely to be incorrect. """

  derpName = _Attribute()
  realName = _Attribute()

  def __init__(self, realName: str, derpName: str, ) -> None:
    self.__derp_name__ = derpName
    self.__real_name__ = realName
    SyntaxError.__init__(self, )

  def __str__(self) -> str:
    """String representation of the QuestionableSyntax."""
    spec = """%s! Received name '%s' which is similar enough to '%s' to be a 
    likely typo. """
    cls = type(self).__name__
    info = spec % (cls, self.derpName, self.realName)
    return monoSpace(info)

  __repr__ = __str__
