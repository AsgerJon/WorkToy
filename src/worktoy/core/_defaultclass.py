"""WorkToy - DefaultClass
This class provides utility as static methods.
Classes in the package subclass this class.

Baseclasses in order of appearance:
 - PrimitiveClass
 - ParsingClass
 - ExceptionClass
 - DefaultClass (this)
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import ExceptionClass


class DefaultClass(ExceptionClass):
  """WorkToy - DefaultClass
  This class provides utility as static methods.
  Classes in the package subclass this class.
  """

  def __init__(self, *args, **kwargs) -> None:
    ExceptionClass.__init__(self, *args, **kwargs)
