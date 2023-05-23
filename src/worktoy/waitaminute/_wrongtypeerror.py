"""WrongTypeError should be raised where TypeError would be raised,
but with more specific information. If the type is 'wrong' because the
type found is NoneType, that is not really a type error. In that case,
raise a ProceduralError because it is likely because the variable had not
yet been initialised. """
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import ExceptionCore


class WrongTypeError(ExceptionCore):
  """WrongTypeError should be raised where TypeError would be raised,
  but with more specific information. If the type is 'wrong' because the
  type found is NoneType, that is not really a type error. In that case,
  raise a ProceduralError because it is likely because the variable had not
  yet been initialised.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def parseTypes(self, *args, **kwargs) -> tuple[Any, type]:
    """Parses types from arguments"""
    raise NotImplementedError

  def __init__(self, *args, **kwargs) -> None:
    ExceptionCore.__init__(self, *args, **kwargs)

  def _createMsg(self, *args, **kwargs) -> str:
    """Reimplementation"""
    expectedType, actualType = args[1], type(args[0])
    msg = """Expected to receive %s, but actually received: %s!"""
    self._msg = msg % (expectedType, actualType)
    return self._msg
