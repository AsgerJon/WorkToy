"""
DispatchException is raised when a 'Dispatcher' cannot resolve the given
arguments to a registered overload.
"""
#  Apache-2.0 license
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
    """Render the dispatch failure as a got-then-expected report."""
    from ...dispatch import TypeSig
    owner = self.dispatch.__field_owner__  # adjust to the real owner attr
    name = '%s.%s' % (owner.__name__, self.dispatch.__field_name__)
    received = '<br><tab><tab>'.join(
      '<%s %s>' % (type(a).__name__, repr(a)) for a in self.args
    )
    argSig = str(TypeSig.fromArgs(*self.args))
    available = '<br><tab><tab>'.join(
      str(sig) for sig, _ in self.dispatch.__sig_funcs__
    )
    lines = [
      """no overload of '%s' accepts these arguments:""" % name,
      """<tab>received:<br><tab><tab>%s""" % received,
      """<tab>argument signature: %s""" % argSig,
      """<tab>available signatures:<br><tab><tab>%s""" % available,
    ]
    return textFmt('<br>'.join(lines))

  __repr__ = __str__
