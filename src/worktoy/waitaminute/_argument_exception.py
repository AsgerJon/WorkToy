"""ArgumentException is a custom exception class that inherits from
ValueError. It should be raised when the number of arguments passed to a
callable is not supported."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace


class ArgumentException(ValueError):
  """ArgumentException is a custom exception class that inherits from
  ValueError. It should be raised when the number of arguments passed to a
  callable is not supported."""

  def __init__(self, fName: str, *args) -> None:
    """Initializes the ArgumentException. """
    e = self.parseArgs(fName, *args)
    ValueError.__init__(self, e)

  @classmethod
  def parseArgs(cls, fName: str, *args) -> str:
    """Parses the arguments passed to the function. """

    intArgs = []
    for arg in args:
      if isinstance(arg, int) and arg not in intArgs:
        intArgs.append(arg)

    if not intArgs:
      return """Function named: '%s' received an unexpected number of 
      arguments!""" % fName
    if len(intArgs) == 1:
      n = intArgs[0]
      if not n:
        e = """Function '%s' received no arguments which is not supported!"""
      elif n == 1:
        e = """Function '%s' received 1 argument which is not supported!"""
      else:
        e = """Function '%%s' received %d arguments which is not 
        supported!""" % n
      return e % fName
    if len(intArgs) == 2:
      nAct, nExp = intArgs
      strAct, strExp = None, None
      if not nAct:
        strAct = "no arguments"
      elif nAct == 1:
        strAct = "1 argument"
      else:
        strAct = "%d arguments" % nAct
      if not nExp:
        strExp = "no arguments"
      elif nExp == 1:
        strExp = "1 argument"
      else:
        strExp = "%d arguments" % nExp
      return monoSpace("""Function '%s' received %s but expected 
      %s!""" % (fName, strAct, strExp))
    nAct = intArgs[0]
    nMin, nMax = min(intArgs[1:]), max(intArgs[1:])
    if nMin < nAct < nMax:
      return cls.parseArgs(fName, )
    strAct, strExp = None, None
    if not nAct:
      strAct = "no arguments"
    elif nAct == 1:
      strAct = "1 argument"
    else:
      strAct = "%d arguments" % nAct
    strExp = "%d to %d arguments" % (nMin, nMax)
    return monoSpace("""Function '%s' received %s but expected
    %s!""" % (fName, strAct, strExp))
