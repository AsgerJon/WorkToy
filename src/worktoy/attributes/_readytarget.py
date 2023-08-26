"""WorkToy - Attributes - ReadyTarget
The ReadyTarget clas wraps target classes with general functionality used
by attributes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import DefaultClass


class ReadyTarget(DefaultClass):
  """WorkToy - Attributes - ReadyTarget
  The ReadyTarget clas wraps target classes with general functionality used
  by attributes."""

  _attributes = None

  @classmethod
  def getAttributes(cls) -> list:
    """Getter-function for the attributes assigned to the target class. """

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._hostAttribute = args[0]
    self._targetClass = None

  def getAttributesFactory(self) -> classmethod:
    """Creates getter function as class method on target class for the
    list of attributes. """

    def getAttributes(cls: type, ) -> dict:
      """Getter-function for list of attributes"""
      return getattr(cls, '__attributes__')

    return classmethod(getAttributes)

  def getHostAttribute(self) -> object:
    """Getter-function for the instance of attribute invoked by this
    instance."""
    return self._hostAttribute

  def setTargetClass(self, targetClass: type) -> type:
    """Setter-function for target class"""
    self._targetClass = targetClass
    if not getattr(targetClass, '__attribute_ready__', False):
      getAttributes = self.getAttributesFactory()
      setattr(targetClass, '__attribute_ready__', True)
      setattr(targetClass, '__attributes__', {})
      setattr(targetClass, 'getAttributes', getAttributes)
    return self._targetClass

  def getTargetClass(self) -> type:
    """Getter-function for the target class"""
    return self._targetClass

  def __call__(self, *args, **kwargs) -> object:
    """If the target class is not set, the first positional argument is
    expected to provide a target class.
    Otherwise, the call is passed on to the target class."""
    if self._targetClass is None:
      if args and args[0] is not None and isinstance(args[0], type):
        return self.setTargetClass(args[0])
      raise TypeError
    targetClass = self.getTargetClass()
    return targetClass(*args, **kwargs)
