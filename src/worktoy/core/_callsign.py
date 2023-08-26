"""WorkToy - Core - CallSign
Specifies argument types of a function."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from types import GenericAlias

from worktoy.core import ParsingClass

Argument = tuple[str, type]
Arguments = tuple[Argument, ...]
Signature = tuple[Arguments, Argument]
Types = tuple[type, ...]
Names = tuple[str, ...]

Signature.__text_signature__


class CallSign(ParsingClass):
  """WorkToy - Core - CallSign
  Specifies argument types of a function."""

  @staticmethod
  def isSignature(signature: GenericAlias) -> bool:
    """Replacement for """

  def __init__(self, *args: type, **kwargs) -> None:
    ParsingClass.__init__(self, *args, **kwargs)
    argNames = [i for i in args if isinstance(i, str)] or ['return', ]
    argTypes = [i for i in args if isinstance(i, type)] or [object, ]
    msg = """Inconsistent arguments! Found fewer argument names than 
    types"""
    self._arguments = None
    if len(argTypes) - len(argNames) < 0:
      msg = """Inconsistent arguments! Found more argument names than 
      types!"""
      raise ValueError(self.monoSpace(msg))
    if len(argTypes) - len(argNames) > 1:
      raise ValueError(self.monoSpace(msg))
    if len(argTypes) - len(argNames) == 1 and argNames[-1] == 'return':
      raise ValueError(self.monoSpace(msg))
    if len(argTypes) - len(argNames) == 1 and argNames[-1] != 'return':
      argNames.append('return')
    if len(argTypes) == len(argNames) and argNames[-1] == 'return':
      self._arguments = {k: v for (k, v) in zip(argNames, argTypes)}
    if self._arguments is None:
      raise TypeError

  def getTypes(self) -> Types:
    """Getter-function for the types."""
    return (*[v for (_, v) in self._arguments.items()],)

  def getNames(self) -> Names:
    """Getter-function for the names."""
    return (*[k for (k, _) in self._arguments.items()],)

  def getReturnType(self) -> type:
    """Getter-function for return type"""
    return self.getTypes()[-1]

  def getReturnName(self) -> str:
    """Getter-function for return name."""
    return 'return'

  def getCallTypes(self) -> Types:
    """Getter-function for call types"""

  def getReturn(self) -> Argument:
    """Getter-function for return"""
    return ('return', self.getTypes()[-1])

  def __contains__(self, signature: Signature) -> bool:
    """Compares against signature"""
    if isinstance(signature, tuple):
      args = signature[0]
      return_ = signature[-1]

  def __len__(self, ) -> int:
    """Length is taken as the number of arguments in the signature
    including the return value. """
    return len(self._arguments.keys())

  def __str__(self, ) -> str:
    """String Representation"""
    header = 'Signature: '
    return 'Signature:\n%s' % (self.__repr__())

  def __repr__(self, ) -> str:
    """Code Representation"""
    args, return_ = '', ''
    for (i, (name, type_)) in enumerate(self._arguments.items()):
      typeNames = [getattr(type_, '__qualname__', None),
                   getattr(type_, '__name__', None), '%s' % type_]
      args += '%s: %s' % (name, self.maybe(typeNames))
      if i < len(self) - 1:
        args += ', '
      else:
        return_ = '%s' % (self.maybe(typeNames))
    return '(%s) -> (%s)' % (args, return_)
