"""ExceptionCore implements basic error/warning functionality."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
from typing import NoReturn, Any, TYPE_CHECKING

from icecream import ic

from worktoy.core import plenty, maybe
from worktoy.stringtools import monoSpace
from worktoy.waitaminute import _ExceptionCoreProperties

if TYPE_CHECKING:
  from worktoy.waitaminute import RaiseIf

ic.configureOutput(includeContext=True)


class ExceptionCore(Exception, _ExceptionCoreProperties):
  """Base class for custom exceptions."""

  @classmethod
  def yoDawg(cls, instance: Any = None) -> ExceptionCore:
    """Heard you like ReadOnlyError, so we put a ReadOnlyError
      in your ReadOnlyError!"""

    msg = """Heard you like ReadOnlyError, so we put a ReadOnlyError
          in your ReadOnlyError!"""
    from worktoy.stringtools import monoSpace
    from worktoy.waitaminute import ReadOnlyError
    return ReadOnlyError(monoSpace(msg))

  def __init__(self, *args, **kwargs) -> None:
    _ExceptionCoreProperties.__init__(self, )
    self._setExceptionContext()
    Exception.__init__(self, self.msg)

  def _setExceptionContext(self) -> NoReturn:
    """Sets the contextual information of the exception."""
    frame = inspect.currentframe()
    # Traverse up the call stack to find the first frame outside the
    # CustomExceptionBase class
    while frame and frame.f_code.co_name == '__init__':
      frame = frame.f_back
    if frame:
      self._callerFunction = frame.f_globals.get('__name__')
      self._callerMethod = frame.f_code.co_name
      self._callerClass = frame.f_locals.get('self')

  def __rrshift__(self, other: RaiseIf) -> NoReturn:
    """LOL"""
    if other:
      raise self

  def createMessage(self) -> NoReturn:
    """Creator-function for message. Implementation of abstract method."""
    words = [self.func, self.insClass, self.meth]
    if not plenty(words):
      return False
    method = '%s.%s' % (self.insClass, self.meth)
    scope = '%s' % (self.func)
    msg = """Something stupid happened during the %s method running the %s 
    scope!""" % (method, scope)
    if self._comment is None:
      comment = """The developer victim could not be reached for comment."""
    elif isinstance(self._comment, str):
      comment = """The developer victim gave the following statement: """
    else:
      self._comment = None
      return self.createMessage()
    message = msg
    head, foot = 77 * '_', 77 * '¨'

    from worktoy.stringtools import justify
    msg = justify(message).replace('\n', '<br>')
    cmt = justify(comment).replace('\n', '<br>')
    print(message)
    print(comment)
    cunt = '\n'.join([head, message, comment, foot])
    self._msg = justify(cunt)
    return True
