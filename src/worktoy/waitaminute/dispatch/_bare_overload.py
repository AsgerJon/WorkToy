"""
BareOverload is raised when '@overload' is written without the
parentheses holding its signature.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class BareOverload(WorkToyException, TypeError):
  """
  BareOverload is raised when '@overload' or '@overload.flex' is written
  without the parentheses holding the classes of its signature, as
  'typing.overload' is written. The decorator then receives the function
  where it expects the first class of the signature, and the mistake used
  to be refused as a function that is no class, which did not say that
  the parentheses were missing. It is refused at the decorator, naming the
  function and the form with parentheses. It subclasses 'TypeError', as
  the refusal of an entry that is no class does.

  Attributes
  ----------
  decorator : str
    The decorator written without parentheses, 'overload' or
    'overload.flex'.
  func : Any
    What the decorator received: the function, possibly under a
    'classmethod' or 'staticmethod', or the record of another decorator.
  """

  __slots__ = ('decorator', 'func')

  def __init__(self, decorator: str, func: Any) -> None:
    self.decorator = decorator
    self.func = func
    TypeError.__init__(self, )

  def __str__(self) -> str:
    spec = """'@%s' is written without parentheses over '%s'. It takes the
    classes of the signature in parentheses, as '@%s(int)', and '@%s()'
    for a call with no positional argument."""
    try:
      name = object.__getattribute__(self.func, '__qualname__')
    except AttributeError:
      #  This branch is reached by the following:
      #  - The decorator received a record of another decorator, or a
      #    'classmethod' or 'staticmethod' object before Python 3.10
      name = repr(self.func)
    decorator = self.decorator
    return textFmt(spec % (decorator, name, decorator, decorator))

  __repr__ = __str__
