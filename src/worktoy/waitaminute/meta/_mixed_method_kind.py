"""
MixedMethodKind is raised when the declarations of one overloaded name
are not all one kind of method, or when one is decorated as both a
classmethod and a staticmethod.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional


class MixedMethodKind(WorkToyException, SyntaxError):
  """
  MixedMethodKind is raised when the declarations of one overloaded name
  are not all one kind of method. One dispatcher stands at the name, and
  it passes the instance, the class or nothing ahead of the arguments of
  every call, so every declaration at the name is an instance method, or
  every one is decorated '@classmethod', or every one '@staticmethod'. A
  function decorated as both a classmethod and a staticmethod is refused
  as well: Python itself gives that stack a different meaning on each
  version, refusing the call on 3.7 and 3.8, acting as a staticmethod on
  3.9 to 3.12 and as a classmethod from 3.13. The refusal comes at the
  declaration breaking the rule, from the decorator for a stack under
  '@overload' and from the class body otherwise. It subclasses
  'SyntaxError', as the other refusals of a class-body line do.

  Attributes
  ----------
  className : str or None
    The name of the class whose body declares the name, or None when a
    decorator refuses a stack before any class exists.
  overloadName : str
    The overloaded name, or the name of the function a decorator refused.
  kinds : tuple
    The two kinds that disagree, each 'classmethod', 'staticmethod' or
    None for an instance method: the earlier declaration first, or the
    outer decorator of a stack.
  """

  __slots__ = ('className', 'overloadName', 'kinds',)

  def __init__(
      self,
      className: Optional[str],
      overloadName: str,
      kinds: tuple,
  ) -> None:
    self.className = className
    self.overloadName = overloadName
    self.kinds = kinds
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  @staticmethod
  def _describeKind(kind: Any) -> str:
    if kind is None:
      return 'an instance method'
    return """a '%s'""" % kind.__name__

  def __str__(self) -> str:
    if self.className is None:
      name = self.overloadName
    else:
      name = '%s.%s' % (self.className, self.overloadName)
    first, second = self.kinds
    spec = """The overloaded name '%s' is declared as %s and as %s."""
    info = spec % (
      name, self._describeKind(first), self._describeKind(second),
    )
    rule = """Every declaration at an overloaded name is an instance
    method, or every one is decorated '@classmethod', or every one
    '@staticmethod', and none is decorated as both."""
    return textFmt(info, rule)

  __repr__ = __str__
