"""InvalidNameSpaceError is a custom Exception raised by the WorkTypeMeta
class when an object intended for use as the name space returned by the
prepare method fails validation checks. For each possible case an
appropriate message is included."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import MutableMapping, Any

from worktoy.stringtools import monoSpace

Map = MutableMapping[str, Any]


class InvalidNameSpaceError(Exception):
  """InvalidNameSpaceError is a custom Exception raised by the WorkTypeMeta
  class when an object intended for use as the name space returned by the
  prepare method fails validation checks. For each possible case an
  appropriate message is included."""

  @staticmethod
  def _getErrorMessage(errorCase: int, obj: Map) -> str:
    """Getter-function for the error message associated with errorCase"""
    req = ['__getitem__', '__setitem__', '__contains__']
    if errorCase == 1:
      msg = """One or more of the required methods are missing 
      from the __dict__ of the object! Specifically, the following are 
      missing:"""
      mis = '<br>  '.join([m for m in req if getattr(obj, m, None) is None])
      return monoSpace('%s<br>%s' % (msg, mis))
    if errorCase == 2:
      msg = """Mismatch between value inserted at key and value returned 
      from key!"""
      return monoSpace(msg)
    if errorCase == 3:
      msg = """Failure to recognize key that were attempted set"""
      return monoSpace(msg)
    if errorCase == 4:
      msg = """Failure of the __contains__ method to correctly recognize 
      set key!"""
      return monoSpace(msg)
    if errorCase == 5:
      msg = """Encountered unexpected exception. An instance of KeyError 
      was expected!"""
      return monoSpace(msg)
    if errorCase == 6:
      msg = """When attempting to retrieve a value at a key not supported 
      by the mapping object, the expected KeyError were never raised. 
      Please note that using a mapping object that fails to raise a 
      KeyError under these circumstances, will lead to highly undefined 
      behaviour!"""
      return monoSpace(msg)
    e = """The given integer %d did not match a supported error case!"""
    raise ValueError(monoSpace(e % errorCase))

  def __init__(self, errorCase: int, obj: Any, *args) -> None:
    Exception.__init__(self, self._getErrorMessage(errorCase, obj), *args, )
