"""
DelException is a custom exception raised when someone attempts to create
a class that implements the '__del__' method without providing the custom
keyword argument: 'trustMeBro=True'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Never


class DelException(SyntaxError):
  """
  DelException is a custom exception raised when someone attempts to create
  a class that implements the '__del__' method without providing the custom
  keyword argument: 'trustMeBro=True'.
  """

  mcls: _Attribute()
  name: _Attribute()
  bases: _Attribute()

  def __init__(self, *args) -> None:
    """Initialize the DelException with the class."""
    _mcls, _name, _bases = None, None, None

    for arg in args:
      if isinstance(arg, type) and _mcls is None:
        _mcls = arg
        continue
      if isinstance(arg, str) and _name is None:
        _name = arg
        continue
      if isinstance(arg, tuple) and _bases is None:
        for base in arg:
          if not isinstance(base, type):
            break
        else:
          _bases = arg
          continue
      if all(i is not None for i in (_mcls, _name, _bases)):
        break

    if _mcls is not None:
      self.mcls = _mcls
    if _name is not None:
      self.name = _name
    if _bases is not None:
      self.bases = _bases

    SyntaxError.__init__(self, self.__str__())

  def __str__(self) -> str:
    """Return a string representation of the DelException."""
    infoSpec = """When attempting to derive a class named '%s' from the 
    metaclass '%s', the '__del__' method was found in the namespace! This 
    is almost always a typo, but if not this error can be suppressed by 
    passing the keyword argument 'trustMeBro=True' during class creation. """
    if self.bases:
      mclsSpec = """%s with bases: (%s)"""
    else:
      mclsSpec = """%s%s"""
    basesStr = ', '.join(base.__name__ for base in self.bases)
    mclsName = mclsSpec % (self.mcls.__name__, basesStr)
    info = infoSpec % (self.name, mclsName)
    return info
