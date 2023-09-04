"""WorkToy - Wait A Minute! - DispatcherException
This exception should be raised when a dispatcher fails to match a
function call to any overloaded functions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.waitaminute import MetaXcept


class DispatcherException(MetaXcept):
  """WorkToy - Wait A Minute! - DispatcherException
  This exception should be raised when a dispatcher fails to match a
  function call to any overloaded functions."""

  def __init__(self, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._signatures = kwargs.get('signatures', None)
    self._args = kwargs.get('args', None)
    if self._signatures is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_signatures')
    if self._args is None:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('_args')
    ic(self._signatures)
    ic(self._args)

  def __str__(self) -> str:
    header = MetaXcept.__str__(self)
    argHeader = 'Dispatcher received arguments:'
    argBody = ', '.join([str(arg) for arg in self._args])
    argBody = '(%s)' % argBody
    sigHeader = 'and the following signatures:'
    sigLines = []
    for signature in self._signatures:
      line = ', '.join([arg.__qualname__ for arg in signature])
      sigLines.append('(%s)' % line)
    sigBody = '<br>'.join(sigLines)

    msg = '%s<br>%s<br>%s<br>%s' % (argHeader, argBody, sigHeader, sigBody)
    return '%s\n%s' % (header, self.monoSpace(msg))
