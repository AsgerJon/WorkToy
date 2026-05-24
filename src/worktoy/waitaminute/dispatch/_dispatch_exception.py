"""DispatchException is raised when a 'Dispatcher' fails to resolve a
matching function from the given arguments. Because the overload protocol
relies on type matching, this exception subclasses 'TypeError' so existing
error handlers catch it.
"""
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
  DispatchException is raised when a 'Dispatcher' fails to resolve the
  given arguments to a matching function.

  Attributes
  ----------
  dispatch : Dispatcher
    The 'Dispatcher' that failed to dispatch the arguments. When raising
    this exception by hand, a static type checker sees the relevant
    objects as 'overload' instances even though at runtime they are
    'Dispatcher' instances; the type hint admits both so the checker does
    not flag a mismatch.
  args : tuple
    The arguments that could not be dispatched.
  """

  __slots__ = ('dispatch', 'args')

  def __init__(self, dispatch: Overloaded, args: Args, ) -> None:
    self.dispatch = dispatch
    self.args = args
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Dispatcher object: <br><tab><tab>%s <br><tab>failed to 
    dispatch arguments: 
    <br><tab><tab>%s<br><tab>matching type signature: <br><tab><tab> 
    '%s'<br>
    The 'Dispatcher' object supports the following type signatures:
    <br><tab><tab>%s<br>
    """
    dispStr = str(self.dispatch)
    args = (*('<%s %s>' % (type(a).__name__, repr(a)) for a in self.args),)
    argsStr = '<br><tab><tab>'.join(str(arg) for arg in args)
    signatures = (*(sig for sig, _ in self.dispatch.__sig_funcs__),)
    sigStr = '<br><tab><tab>'.join(str(sig) for sig in signatures)
    from ...dispatch import TypeSig
    typeStr = str(TypeSig.fromArgs(*self.args))
    info = infoSpec % (dispStr, argsStr, typeStr, sigStr)
    return textFmt(info, )

  __repr__ = __str__
