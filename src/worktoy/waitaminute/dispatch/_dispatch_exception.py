"""
DispatchException is raised when a 'Dispatcher' cannot resolve the given
arguments to a registered overload.
"""
#  Apache-2.0 license
#  Copyright (c) 2024-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, TypeAlias, Union

  Args: TypeAlias = tuple[Any, ...]
  Excs: TypeAlias = tuple[Exception, ...]

  from worktoy.dispatch import Dispatcher
  from worktoy.dispatch import overload

  Overloaded: TypeAlias = Union[Dispatcher, overload]
  #  At runtime, the 'overload' objects will be replaced with 'Dispatcher'
  #  objects, but that is not visible to type checkers.


class DispatchException(WorkToyException, TypeError):
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
  posArgs : tuple
    The positional arguments that could not be dispatched.
  keyArgs : dict
    The keyword arguments of the call, empty when it had none. A
    keyword call binds to the parameter names of each registration, so
    the message lists the names received where the call missed.
  """

  __slots__ = ('dispatch', 'posArgs', 'keyArgs')

  def __init__(
      self,
      dispatch: Overloaded,
      args: Args,
      kwargs: Optional[dict] = None,
  ) -> None:
    self.dispatch = dispatch
    self.posArgs = args
    self.keyArgs = dict() if kwargs is None else kwargs
    TypeError.__init__(self, )

  def __str__(self) -> str:
    """Render the dispatch failure as a got-then-expected report."""
    from ...dispatch import TypeSig
    owner = self.dispatch.__field_owner__
    name = '%s.%s' % (owner.__name__, self.dispatch.__field_name__)
    received = '<br><tab><tab>'.join(
      '<%s %s>' % (type(a).__name__, repr(a)) for a in self.posArgs
    ) or '(none)'
    argSig = str(TypeSig.fromArgs(*self.posArgs))
    #  A variadic declaration shows as itself, not as the concrete
    #  signatures expanded from it for short calls.
    sigs = self.dispatch._getDeclaredSigs()
    available = '<br><tab><tab>'.join(str(sig) for sig in sigs) or '(none)'
    lines = [
      """no overload of '%s' accepts these arguments:""" % name,
      """<tab>received:<br><tab><tab>%s""" % received,
    ]
    if self.keyArgs:
      keywords = ', '.join(self.keyArgs)
      lines.append("""<tab>received keywords: %s""" % keywords)
    lines += [
      """<tab>argument signature: %s""" % argSig,
      """<tab>available signatures:<br><tab><tab>%s""" % available,
    ]
    return textFmt('<br>'.join(lines))

  __repr__ = __str__
