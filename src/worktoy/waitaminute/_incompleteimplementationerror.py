"""IncompleteImplementationError Exception
**This code was written by Chat-GPT August 3 Version**

This exception is raised when a subclass, such as `CustomModel`, does not
fully implement the required methods or properties specified by its base
class, such as `AbstractModel`.

It serves to signal to developers that they have created a subclass missing
key implementations expected by its base class.

For example, if `AbstractModel` is a base class that expects its subclasses
to implement a method named `processData`, and a subclass `CustomModel` does
not provide this implementation, this exception can be raised to alert the
developer to this missing implementation.

Example Usage:
--------------
class AbstractModel:
    pass

class CustomModel(AbstractModel):
    pass

customModel = CustomModel()
val = getattr(customModel, 'processData', None)

if val is None:
    raise IncompleteImplementationError(
      AbstractModel, customModel, 'processData')

This raises an IncompleteImplementationError indicating that the
'CustomModel' class must implement the 'processData' method when subclassing
'AbstractModel'.

Attributes:
-----------
_baseClass : type
    The base class that the subclass is expected to extend.
_object : object
    The instance missing the method/attribute implementation.
_methodName : str
    The name of the missing method or attribute from the subclass.

Methods:
--------
_getMessage(self) -> str
    Constructs and returns the customized error message.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import AbstractError


class IncompleteImplementationError(AbstractError):
  """
  Raised when a subclass does not fully implement the required methods
  or properties. Initialize the IncompleteImplementationError exception.

    :param baseClass: The base class that must be subclassed
    :param obj: The instance of the subclass that is missing a
      method/attribute
    :param methodName: The name of the missing method/attribute
  """

  def __init__(self,
               baseClass: type,
               obj: object,
               methodName: str,
               **kwargs) -> None:
    self._baseClass = baseClass
    self._methodName = methodName
    self._msgSpec = kwargs.get('msgSpec', None)
    AbstractError.__init__(self, obj)

  def _getTemplate(self) -> str:
    """Getter-function for the template"""
    defVal = """Subclasses of %s must implement the %s method. This method 
      is missing from the custom subclass %s"""
    return defVal if self._msgSpec is None else self._msgSpec

  def _getMessage(self) -> str:
    """
    Provides a customized error message indicating the incomplete
    implementation.
    """
    cls = self._baseClass
    call = self._methodName
    sub = self._baseClass.__class__.__qualname__
    template = self._getTemplate()
    argCount = len(template) - len(template.replace('%s', ' '))
    args = [arg for arg in [cls, call, sub] if arg is not None]
    if len(args) != argCount:
      raise ValueError
    return self.monoSpace(template % (*args,))
