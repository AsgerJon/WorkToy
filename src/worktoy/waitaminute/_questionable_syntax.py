"""QuestionableSyntax is raised when a name is encountered that is likely
a typo, such as '__set_item__' instead of '__setitem__' or '__setname__'
instead of '__set_name__'.
This is a"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.text import monoSpace

if TYPE_CHECKING:
  from typing import Any, Callable

  # Placeholder for the actual types used in the code.
  CallMeMaybe = Callable[..., Any]
  Self = Any


class _Name:
  """Represents a name in the code. """

  __pvt_name__ = None

  def __init__(self, name: str) -> None:
    self.__pvt_name__ = name

  def __get__(self, instance: object, owner: type) -> Any:
    if instance is None:
      return self
    return getattr(instance, self.__pvt_name__)


class QuestionableSyntax(SyntaxError):
  """QuestionableSyntax is raised when a name is encountered that is likely
  a typo, such as '__set_item__' instead of '__setitem__' or '__setname__'
  instead of '__set_name__'.
  This is a subclass of SyntaxError and should be used to indicate that
  the code is likely to be incorrect. """

  __derp_name__ = None
  __real_name__ = None

  derpName = _Name('__derp_name__')
  realName = _Name('__real_name__')

  def __init__(self, derpName: str, realName: str) -> None:
    self.__derp_name__ = derpName
    self.__real_name__ = realName
    info = """Received name: '%s' which is similar enough to '%s' to be a 
    likely typo. """
    SyntaxError.__init__(self, monoSpace(info % (derpName, realName)))
