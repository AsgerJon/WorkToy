"""AnnotationError should be raised when a function does have proper
annotations in place, but where the types hinted differ from expectations."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from worktoy.core import searchKeys, CallMeMaybe, plenty, empty
from worktoy.stringtools import stringList
from worktoy.waitaminute import ExceptionCore


class AnnotationError(ExceptionCore):
  """AnnotationError should be raised when a function does have proper
  annotations in place, but where the types hinted differ from expectations.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    ExceptionCore.__init__(self, *args, **kwargs)

  def _createMsg(self, *args, **kwargs) -> str:
    """Reimplementation"""
    return_ = searchKeys('return_', 'return') @ str >> kwargs
    functionKeys = stringList('func, function, ')
    function_ = searchKeys(*functionKeys) @ CallMeMaybe >> kwargs
    msg = """When analyzing function: %s for annotation mismatches, 
    the following problems were encountered: \n"""
    returnMsg, posMsg = '', ''
    if return_:
      e, a = [return_.get(k, None) for k in stringList('expected, actual')]
      if empty(e, a):
        returnMsg = 'Return type mismatch'
      if plenty(e, a):
        returnMsg = """Expected function to return a type %s, but function 
        annotation indicated %s!""" % (e, a)
      if e is None:
        returnMsg = """Function annotates unexpected return type: %s""" % a
      if a is None:
        returnMsg = """Function annotated return type does not match the 
        expected return type which is: %s""" % e
    if args:
      posMsg = """The function were expected to require the following 
      types, but these could not be found in the function annotations:"""
      for arg in args:
        posMsg += ('\n  %s' % arg)
    allMsg = [m for m in [msg, returnMsg, posMsg] if m]
    self._msg = '\n'.join(allMsg)
    return self._msg
