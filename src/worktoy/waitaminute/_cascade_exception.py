"""
CascadeException provides a custom exception raised to indicate that a
system of exceptions occurred in a cascading manner after a series of
failed fallbacks. This aims at solving the same as ExceptionGroup,
but this is available only for python 3.11+.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..parse import maybe
from ..text import monoSpace, wordWrap

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Iterator, Self


class CascadeException(Exception):
  """
  CascadeException provides a custom exception raised to indicate that a
  system of exceptions occurred in a cascading manner after a series of
  failed fallbacks. This aims at solving the same as ExceptionGroup,
  but this is available only for python 3.11+.

  When instantiating provide the exceptions in the order caught.
  """

  exceptionChain = _Attribute()

  # def __new__(cls, *exceptions: Exception) -> Exception:
  #   """
  #   Create a new CascadeException instance with the given exceptions.
  #   """
  #   for exception in exceptions:
  #     if isinstance(exception, Exception):
  #       continue
  #     if isinstance(exception, BaseException):
  #       raise exception
  #   if len(exceptions) == 1:
  #     out = exceptions[0]
  #     setattr(out, '__no_init__', True)
  #     out.__cause__ = cls()
  #     return out
  #   if len(exceptions) == 2:
  #     out = exceptions[0]
  #     exceptions[1].__cause__ = cls()
  #     out.__cause__ = exceptions[1]
  #     setattr(out, '__no_init__', True)
  #     return out
  #   return Exception.__new__(cls)

  def __init__(self, *exceptions: Exception) -> None:
    """
    Initialize the CascadeException with a chain of exceptions.
    """
    self.exceptionChain = exceptions

  def __str__(self, ) -> str:
    """
    Get the string representation of the CascadeException.
    """
    if not self.exceptionChain:
      return Exception.__str__(self)
    headerSpec = """%s!\nA total of %d exceptions were raised in cascading 
    manner:"""
    clsName = type(self).__name__
    header = monoSpace(headerSpec % (clsName, len(self)))
    lines = []
    for (i, e) in enumerate(self):
      infoSpec = """%s!<br>%s"""
      head = '%s%s' % ((i + 2) * '-', type(e).__name__)
      body = wordWrap(73 - 2 * i, repr(e), ).split('\n')
      body = ('%s    <br>' % ' ' * i * 2).join([*body, ])
      lines.append(infoSpec % (head, body))
    lineStr = '<br>'.join(lines)
    return monoSpace("""%s<br>%s""" % (header, lineStr))

  def __repr__(self, ) -> str:
    """
    Code representation of the CascadeException.
    """
    body = ',<br><tab>'.join([repr(e) for e in self])
    clsName = type(self).__name__
    return monoSpace('%s(<br><tab>%s<br>)' % (clsName, body))

  def __iter__(self) -> Iterator[Exception]:
    """
    Iterate over the chain of exceptions.
    """
    for link in maybe(self.exceptionChain, []):
      yield link

  def __contains__(self, exception: Exception) -> bool:
    """
    Check if the given exception is in the chain of exceptions.
    """
    for link in self:
      if link is exception:
        return True
    else:
      return False

  def __len__(self, ) -> int:
    """
    Get the length of the chain of exceptions.
    """
    if self.exceptionChain:
      return len(self.exceptionChain)
    return 0

  def _resolveOther(self, other: Any) -> Self:
    """
    Resolve the other object to a CascadeException if possible.
    """
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, (tuple, list)):
      for item in other:
        if not isinstance(item, Exception):
          break
      else:
        return cls(*other)
    return NotImplemented

  def __eq__(self, other: Any) -> bool:
    """
    Check if the other object is a CascadeException and has the same
    exception chain.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    if len(self) != len(other):
      return False
    for selfLink, otherLink in zip(self, other):
      if selfLink is not otherLink:
        return False
    return True
