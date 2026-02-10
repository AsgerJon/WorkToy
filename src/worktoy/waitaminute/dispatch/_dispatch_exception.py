"""DispatchException provides a custom exception raised when an instance
of OverloadDispatcher fails to resolve the correct function from the
given arguments. Because the overload protocol relies on type matching,
this exception subclasses TypeError such that it can be caught by external
error handlers. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Union

  Args: TypeAlias = tuple[Any, ...]
  Excs: TypeAlias = tuple[Exception, ...]

  from worktoy.dispatch import Dispatcher
  from worktoy.dispatch import overload

  Overloaded: TypeAlias = Union[Dispatcher, overload]
  #  At runtime, the 'overload' objects will be replaced with 'Dispatcher'
  #  objects, but that is not visible to type checkers.


class DispatchException(TypeError):
  """
  DispatchException provides a custom exception raised to indicate that a
  'Dispatcher' object failed to resolve given arguments to a matching
  function object.

  Arguments:
    dispatch: The 'Dispatcher' object that failed to dispatch the given
    arguments. (When manually raising this exception, the static type
    checker will recognize the relevant objects as 'overload' objects,
    but at runtime these will be replaced with 'Dispatcher' objects.
    Hinting both types prevents type checkers from indicating type
    mismatch.)
    args: The arguments that could not be dispatched
  """

  __slots__ = ('dispatch', 'args')

  def __init__(self, dispatch: Overloaded, args: Args, ) -> None:
    self.dispatch = dispatch
    self.args = args
    TypeError.__init__(self, )

  def __str__(self) -> str:
    """
    Return a string representation of the DispatchException.
    """
    infoSpec = """Dispatcher object: '%s' failed to dispatch arguments: 
    <br><tab>%s<br><tab>matching type signature: '%s'<br>"""
    dispStr = str(self.dispatch)
    argsStr = ', '.join(str(arg) for arg in self.args)
    from ...dispatch import TypeSig
    typeStr = str(TypeSig.fromArgs(*self.args))
    info = infoSpec % (dispStr, argsStr, typeStr)
    return textFmt(info, )

  __repr__ = __str__
