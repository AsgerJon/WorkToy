"""ExceptionCore implements basic error/warning functionality."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
import inspect
from typing import NoReturn, Any, Never

from worktoy import maybe, monoSpace, searchKeys


class ExceptionCore(Exception):
  """Base class for custom exceptions."""

  def __init__(self, *args, **kwargs) -> None:
    self._callerInstance = None
    self._callerClass = None
    self._callerFunction = None
    self._callerMethod = None
    ExceptionCore.__init__(self, *args, **kwargs)

  def _getInstance(self) -> Any:
    """Getter-function for instance"""
    return self._callerInstance

  def _setInstance(self, *_) -> Any:
    """Setter deleter function"""
    raise ReadOnlyError('instance')

  def _delInstance(self) -> Any:
    """Illegal deleter function"""
    raise ReadOnlyError('instance')

  def _getClass(self, ) -> Any:
    """Getter-function for class"""
    return self._callerClass

  def _setClass(self, *_) -> Any:
    """Setter deleter function"""
    raise ReadOnlyError('callerClass')

  def _delClass(self) -> Any:
    """Illegal deleter function"""
    raise ReadOnlyError('callerClass')

  def _getCallerFunction(self, ) -> Any:
    """Getter-function for caller function"""
    return self._callerFunction

  def _setCallerFunction(self, *_) -> Any:
    """Setter setter function"""
    raise ReadOnlyError('callerFunction')

  def _delCallerFunction(self) -> Any:
    """Illegal deleter function"""
    raise ReadOnlyError('callerFunction')

  def _getCallerMethod(self, ) -> Any:
    """Getter-function for caller function"""
    return self._callerMethod

  def _setCallerMethod(self, *_) -> Any:
    """Setter setter function"""
    raise ReadOnlyError('callerMethod')

  def _delCallerMethod(self) -> Any:
    """Illegal deleter function"""
    raise ReadOnlyError('callerMethod')

  instance = property(_getInstance, _setInstance, _delInstance)
  insClass = property(_getClass, _setClass, _delClass)
  callerMethod = property(
    _getCallerMethod, _setCallerMethod, _delCallerMethod)
  callerFunction = property(
    _getCallerFunction, _setCallerFunction, _delCallerFunction)

  def _setExceptionContext(self) -> NoReturn:
    """Sets the contextual information of the exception."""
    frame = inspect.currentframe()
    # Traverse up the call stack to find the first frame outside the
    # CustomExceptionBase class
    while frame and frame.f_code.co_name == '__init__':
      frame = frame.f_back

    if frame:
      self._callerFunction = frame.f_globals.get('__name__')
      self._callerMethod = frame.f_code.co_name
      self._callerClass = frame.f_locals.get('self')

  @abstractmethod
  def __str__(self) -> str:
    """Subclasses are required to implement the messaging."""


class ReadOnlyError(ExceptionCore):
  """Custom exception for read-only operations.
  Attributes:
      varName (str): Name of the variable.
      function (str): Name of the function invoking the error.
      fileName (str): Name of the file where the error occurred.
      lineNumber (int): Line number where the error occurred.
      insName (object): Instance where the error occurred.
      insCls (class): Class of the instance where the error
      occurred."""

  @classmethod
  def yoDawg(cls) -> Exception:
    """Create an exception instance of ReadOnlyError."""
    msg = """Heard you like ReadOnlyError, so we put a ReadOnlyError
          in your ReadOnlyError!"""
    return Exception(monoSpace(msg))

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the ReadOnlyError exception.
    Args:
        *args: Variable arguments.
        **kwargs: Keyword arguments.
    Raises:
        None
    Returns:
        None"""
    args = maybe(args, [None, ])
    variableKwarg = searchKeys('variable', 'var') @ str >> kwargs
    variableArg = args[0]
    self._variableName = maybe(variableKwarg, variableArg, None)
    frame = inspect.currentframe().f_back
    code = frame.f_code
    self._function = inspect.getframeinfo(frame).function
    self._fileName = code.co_filename
    self._lineNumber = frame.f_lineno
    self._instance = frame.f_locals.get('self', )
    self._instanceClass = type(self._instance)
    super().__init__(monoSpace(self.__str__()))

  def __str__(self) -> str:
    """Return a string representation of the exception.
    Returns:
        str: String representation of the exception."""
    msg = "Tried to access %s belonging to %s of class %s using %s, " \
          "which is not a permitted operation!"
    msg = monoSpace(msg % (
      self.varName, self.insName, self.insCls, self.function))
    return msg

  def _getVariable(self) -> str:
    """Getter-function for the name of the variable.
    Returns:
        str: Name of the variable."""
    return maybe(self._variableName, 'unnamed')

  def _setVariable(self, *_) -> Never:
    """Illegal setter function.
    Args:
        *_: Variable arguments.
    Raises:
        ReadOnlyError: Always raised to indicate that setting the variable
        is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _delVariable(self) -> Never:
    """Illegal deleter function.
    Raises:
        ReadOnlyError: Always raised to indicate that deleting the
        variable is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _getFunction(self) -> str:
    """Getter-function for the function invoking the error.
    Returns:
        str: Name of the function."""
    return self._function

  def _setFunction(self, *_) -> Never:
    """Illegal setter function.
    Args:
        *_: Variable arguments.
    Raises:
        ReadOnlyError: Always raised to indicate that setting the function
        is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _delFunction(self) -> Never:
    """Illegal deleter function.
    Raises:
        ReadOnlyError: Always raised to indicate that deleting the
        function is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _getFileName(self) -> str:
    """Getter-function for the file name.
    Returns:
        str: File name."""
    return self._fileName

  def _setFileName(self, *_) -> Never:
    """Illegal setter function.
    Args:
        *_: Variable arguments.
    Raises:
        ReadOnlyError: Always raised to indicate that setting the file
        name is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _delFileName(self) -> Never:
    """Illegal deleter function.
    Raises:
        ReadOnlyError: Always raised to indicate that deleting the file
        name is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _getLineNumber(self) -> str:
    """Getter-function for the line number.
    Returns:
        str: Line number."""
    return self._lineNumber

  def _setLineNumber(self, *_) -> Never:
    """Illegal setter function.
    Args:
        *_: Variable arguments.
    Raises:
        ReadOnlyError: Always raised to indicate that setting the line
        number is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _delLineNumber(self) -> Never:
    """Illegal deleter function.
    Raises:
        ReadOnlyError: Always raised to indicate that deleting the line
        number is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _getInstance(self) -> str:
    """Getter-function for the instance.
    Returns:
        str: Instance name."""
    return maybe(self._instance, 'unnamed instance')

  def _setInstance(self, *_) -> Never:
    """Illegal setter function.
    Args:
        *_: Variable arguments.
    Raises:
        ReadOnlyError: Always raised to indicate that setting the instance
        is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _delInstance(self) -> Never:
    """Illegal deleter function.
    Raises:
        ReadOnlyError: Always raised to indicate that deleting the
        instance is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _getInstanceClass(self) -> str:
    """Getter-function for the instance class.
    Returns:
        str: Instance class name."""
    return maybe(self._instanceClass, 'unnamed class')

  def _setInstanceClass(self, *_) -> Never:
    """Illegal setter function.
    Args:
        *_: Variable arguments.
    Raises:
        ReadOnlyError: Always raised to indicate that setting the instance
        class is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  def _delInstanceClass(self) -> Never:
    """Illegal deleter function.
    Raises:
        ReadOnlyError: Always raised to indicate that deleting the
        instance class is not allowed.
    Returns:
        Never"""
    raise self.yoDawg()

  varName = property(_getVariable, _setVariable, _delVariable)
  function = property(_getFunction, _setFunction, _delFunction)
  fileName = property(_getFileName, _setFileName, _delFileName)
  lineNumber = property(_getLineNumber, _setLineNumber, _delLineNumber)
  insName = property(_getInstance, _setInstance, _delInstance)
  insCls = property(_getInstanceClass, _setInstanceClass, _delInstanceClass)
