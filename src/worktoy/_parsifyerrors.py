"""ParsifyError is a custom exception raised by the Parsify class"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from worktoy import searchKeys, maybe, maybeType
from worktoy.sharperexceptions import ReadOnlyError


class ParsifyError(Exception):
  """ParsifyError is a custom exception raised by the Parsify class
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parsifyKwarg = searchKeys('parsify') >> kwargs
    parsifyArg = None
    for arg in args:
      if type(arg).__name__ == 'Parsify' and parsifyArg is None:
        parsifyArg = arg
    self._parsify = maybe(parsifyKwarg, parsifyArg, None)
    if self._parsify is None:
      raise TypeError('Parsify missing!')

  def _getParsify(self) -> Any:
    """Getter-function for the Parsify to whom this error pertains."""
    return self._parsify

  def _setParsify(self, *_) -> Never:
    """Illegal Setter-function"""
    raise ReadOnlyError('parsify')

  def _delParsify(self) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError('parsify')

  parsify = property(_getParsify, _setParsify, _delParsify)


class PositionalArgumentError(ParsifyError):
  """Subclass raised when a parsify tries to use a positional argument it
  does not have access to. Mainly, this prevents double spending of
  arguments. """

  def __init__(self, *args, **kwargs) -> None:
    ParsifyError.__init__(self, *args, **kwargs)
    posArgKwarg = searchKeys('posArg') >> kwargs
    posArgArg = [*args, None][0]
    if posArgArg == self.parsify:
      posArgArg = [*args, None, None][1]
    posArgDefault = None
    self._posArg = maybe(posArgKwarg, posArgArg, posArgDefault)
    if self._posArg is None:
      raise TypeError('Positional argument not found!')

  def __str__(self, ) -> str:
    """String representation"""
    return """Attempted to take argument: %s from Parsify %s, which is not 
    available!""" % (self.posArg, self.parsify)

  def _getPosArg(self) -> Any:
    """Getter-function for the positional argument"""
    return self._posArg

  def _setPosArg(self, *_) -> Never:
    """Illegal Setter-function"""
    raise ReadOnlyError('posArg')

  def _delPosArg(self) -> Never:
    """Illegal deleter-function"""
    raise ReadOnlyError('posArg')

  posArg = property(_getPosArg, _setPosArg, _delPosArg)
