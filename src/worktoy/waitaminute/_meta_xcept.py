"""WorkToy - Wait A Minute! - MetaXcept
Metaclass creating the exception types"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from inspect import FrameInfo, stack, trace
from typing import Never, Any

from icecream import ic

from worktoy.worktoyclass import WorkToyClass
from worktoy.core import Function
from worktoy.metaclass import AbstractMetaClass
from worktoy.waitaminute import ExceptSpace

ic.configureOutput(includeContext=True)


class _MetaXcept(AbstractMetaClass):
  """WorkToy - Wait A Minute! - MetaXcept
  Metaclass creating the exception types"""

  @classmethod
  def __prepare__(mcls, *args, **kwargs) -> dict:
    name, bases = args[0], args[1]
    return ExceptSpace(name, bases, **kwargs)

  def __new__(mcls, *args, **kwargs) -> type:
    name = args[0]
    bases = args[1]
    nameSpace = args[2]
    out = AbstractMetaClass.__new__(mcls, name, bases, nameSpace, **kwargs)
    out.__name_space__ = nameSpace
    return out

  def __init__(cls, *args, **kwargs) -> None:
    name = args[0]
    bases = args[1]
    nameSpace = args[2]
    if isinstance(nameSpace, dict):
      AbstractMetaClass.__init__(cls, name, bases, nameSpace, **kwargs)
    else:
      raise TypeError

  def __call__(cls, *args, **kwargs) -> Exception:
    return AbstractMetaClass.__call__(cls, *args, **kwargs)

  def __eq__(cls, other: type) -> bool:
    """Other must be a type"""
    return True if cls is other else False


class MetaXcept(Exception, WorkToyClass, metaclass=_MetaXcept):
  """In between class exposing the metaclass."""

  def formatHeader(self, header: str) -> str:
    """Formats the given string to a cool header"""
    side = (77 - (len(header) + 6)) / 2
    sideLine = '~' * int(side)
    width = 73 - (2 * side) % 2
    topLine = '| %s |' % (int(width) * '¤')
    bottomLine = '| %s |' % (int(width) * '^')
    coolName = '| %s %s %s |' % (sideLine, header, sideLine)
    return '\n\n%s\n%s\n%s\n' % (topLine, coolName, bottomLine)

  def formatFuncName(self, func: Function) -> str:
    """Assigns name to function."""
    func = getattr(func, '__func__', func)
    funcQualName = getattr(func, '__qualname__', None)
    funcName = getattr(func, '__name__', None)
    funcPrintF = '%s' % func
    return self.maybe(funcQualName, funcName, funcPrintF)

  def formatTypeName(self, type_: type) -> str:
    """Formats the name of a type."""
    if not isinstance(type_, type):
      return self.formatTypeName(type(type_))
    return type_.__qualname__

  def pretty(self, arg: Any) -> str:
    """Formats argument arg."""
    if isinstance(arg, Function):
      return self.formatFuncName(arg)
    if isinstance(arg, type):
      return self.formatTypeName(arg)
    return str(arg)

  def __new__(cls, *args, **kwargs) -> MetaXcept:
    return Exception.__new__(cls)

  def __init__(self, *args, **kwargs) -> None:
    Exception.__init__(self, *args)
    WorkToyClass.__init__(self, *args, **kwargs)
    self._stack = stack()
    self._trace = trace()

  def getStack(self) -> list[FrameInfo]:
    """Getter-function for stack."""
    return self._stack

  def getReversedStack(self) -> list[FrameInfo]:
    """Getter-function for reversed stack."""
    _stack = [i for i in self.getStack()]
    out = []
    while _stack:
      out.append(_stack.pop())
    return out

  def getTrace(self) -> Any:
    """Getter-function for trace"""
    return self._trace

  def getFuncName(self) -> list[str]:
    """Getter-function for the latest function."""
    return [item[-1].function for item in self.getStack()]

  def getFuncQualName(self) -> Function:
    """Getter-function for the qualified names of the functions."""
    return [item.frame.f_code.co_qualname for item in self.getStack()]

  def getFuncs(self) -> Any:
    """Getter-function for functions. FFS"""
    raise NotImplementedError('Intentionally unavailable. Only names.')

  def getSourceFunctionStack(self) -> list:
    """Getter-function for the function stack."""
    out = []
    __exceptional_names__ = self.stringList("""MetaXcept, 
    AbstractMetaClass, _MetaXcept, __guard_validator__""")
    __exceptional_names__.append(self.__class__.__qualname__)
    for item in self.getFuncQualName():
      scope, func = [*item.split('.'), None, None][:2]
      if scope not in __exceptional_names__:
        out.append(item)
    return out

  def getSourceFunctionName(self) -> Any:
    """Getter-function for the function in which the error is raised.
    Unfortunately, only the name is available from the inspect module. """
    return self.getSourceFunctionStack()[-1]

  def getLocals(self) -> Any:
    """Getter-function for locals"""
    out = []
    for item in self.getStack():
      out.append(item.frame.f_locals)
    return out

  def __getattr__(self, key: str) -> object:
    cls = object.__getattribute__(self, '__class__')
    return object.__getattribute__(cls, key)

  def __eq__(self, other: object) -> bool:
    """Implementation of equal operator. Please note that this method
    relates to the instance, not to the class. The class (MetaXcept) has
    its own implementation.
    If other is a type, this method returns MetaXcept == other
    If other is a string:
      self.__str__() == other
    Otherwise:
      self.__str__() == other.__str__()"""
    if isinstance(other, type):
      return self.__class__ == other
    if isinstance(other, str):
      return other in [self.__str__(), self.__class__.__qualname__]
    return self == object.__str__(other)

  def handle(self, *args, **kwargs) -> Never:
    """Should be invoked after the exception is caught. By default,
    it raises itself. """
    raise self

  def __getattribute__(self, key: str) -> Any:
    val = object.__getattribute__(self, key)
    if key == '__module__' and isinstance(val, str):
      return '\n%s\n' % val
    return val

  def __str__(self) -> str:
    """String representation. The default returns the qualified name of
    the error with the new lines above and below."""
    return self.formatHeader(self.__class__.__qualname__)

  def combine(self, other: MetaXcept) -> str:
    """String representation"""
    selfHeader = MetaXcept.__str__(self)
    otherHeader = MetaXcept.__str__(other)
    selfName = self.__class__.__qualname__
    otherName = other.__class__.__qualname__
    title = MetaXcept.__qualname__
    headerContent = """%s encountered multiple errors!""" % title
    subHeaderContent = '%s and %s:' % (selfName, otherName)
    header = self.formatHeader(headerContent)
    subHeader = self.formatHeader(subHeaderContent)
    selfMessage = str(self).replace(selfHeader, '')
    otherMessage = str(other).replace(otherHeader, '')
    return '\n'.join([header, subHeader, selfMessage, otherMessage])

  # def collectInfo(self, ) -> list:
  #   """Collects details for each function step"""
  #   out = []
  #   for f in self.getReversedStack():
  #     out.append(self.collectStepInfo(f))
  #   return out
  #
  # def collectNames(self, ) -> list:
  #   """Collects function names."""
  #
  # def collectStepInfo(self, step: Any) -> dict:
  #   """Collects details for one step"""
  #   globalSnapshot = globals().items()
  #   globalSnapshot = {k: v for (k, v) in globalSnapshot}
  #   name = step.frame.f_code.co_qualname
  #   argNames = step.frame.f_code.co_qualname
  #   func = globalSnapshot.get(name)
  #   note = getattr(func, '__annotations__', None)
  #   if note is None:
  #     return {}
  #   notes = {}
  #   for arg in [*argNames, 'return']:
  #     notes |= {arg: note.get(arg, 'None')}
  #   return dict(name=name, func=func, notes=notes)
  #
  # def funcInfo(self, ) -> Any:
  #   """Function information"""
  #   out = []
  #   for info in self.collectInfo():
  #     if info.get('name', None) != '<module>':
  #       out.append(info)
  #   return out
