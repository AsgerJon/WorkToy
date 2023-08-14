"""ArgumentError should be invoked where required arguments are missing."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.parsing import maybeTypes
from worktoy.stringtools import monoSpace
from worktoy.waitaminute import ReadOnlyError

ic.configureOutput(includeContext=True)


class ArgumentError(Exception):
  """ArgumentError should be invoked where required arguments are missing.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, name: str, *args) -> None:
    self._name = name
    self._key = [arg for arg in args if isinstance(arg, str)]
    self._types = [arg for arg in args if isinstance(arg, type)]
    Exception.__init__(self, name, *args)

  def getName(self) -> str:
    """Getter-function for the name"""
    return self._name

  def setName(self, name: str) -> None:
    """Setter-function for the name"""
    if self._name is None:
      self._name = name
      return
    raise ReadOnlyError('name')

  def _delName(self, *_) -> Never:
    """Illegal deleter method"""
    raise ProtectedPropertyError

  def __str__(self) -> str:
    """String Representation"""
    title = 'ArgumentError for arg: %s' % self._name
    keys = '<br>  '.join(self._key)
    kwHead = monoSpace("""Failed to find argument from the keyword 
      arguments. Tried the following keys:""")
    kwargsMsg = '%s%s' % (kwHead, keys) if keys else ''
    body = """Failed to find argument %s in the positional arguments."""
    typeHead = """The type of %s should have been one of the following"""
    types = '<br>  '.join([str(type_) for type_ in self._types])
