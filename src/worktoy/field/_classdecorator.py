"""ClassDecorator is a subclass of Decorator specifically focused upon
class decorations. Please note that each decorated class should have a
dedicated subclass of this class. To achieve this, please reimplement the
added abstract method 'validateClassIdentity'."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn

from worktoy.core import CallMeMaybe
from worktoy.field import Decorator
from worktoy.waitaminute import n00bError, ValidationError


class ClassDecorator(Decorator):
  """ClassDecorator is a subclass of Decorator specifically focused upon
  class decorations. Please note that each decorated class should have a
  dedicated subclass of this class. To achieve this, please reimplement the
  added abstract method 'validateClassIdentity'.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  @staticmethod
  def whichClass(func: CallMeMaybe) -> type:
    """Returns the class of the function decorators. Subclasses might make
    use of this method when implementing the required abstract method
    'validateClassIdentity'."""
    qName = getattr(func, '__qualname__', None)
    if qName is None:
      raise TypeError('Could not confirm class identity')
    if '.' not in qName:
      raise TypeError('Could not confirm class identity')
    className, funcName, *_ = qName.split('.')

  @abstractmethod
  def validateClassIdentity(self, cls: type) -> type:
    """Each subclass of this class should apply to only one target class.
    Implement this method to ensure that this decorator class is applied
    only to the target class."""

  def validate(self, target: CallMeMaybe) -> NoReturn:
    """Ensures that only functions taking and returning types are
    decorated."""
    target = self.validateClassIdentity(target)
    notes = target.__annotations__
    if not notes:
      raise n00bError('Missing annotations')
    returnFlag, argFlag = False, False
    for (key, val) in notes.items():
      if key == 'return':
        if val == 'type':
          returnFlag = True
      elif val == 'type':
        argFlag = True
    if not (returnFlag and argFlag):
      cause = ''
      head = """Failed to validate target method suitable for use in class 
       decoration. When inspecting the target %s, """ % target
      if not (returnFlag or argFlag):
        cause = """type: 'type' was not found on the return value nor on 
         the argument typehints. """
      elif returnFlag:
        cause = """type: 'type' was found only on the return value, 
         not on any argument value."""
      elif argFlag:
        cause = """type: 'type' was found only on the an argument value, 
         not on the return value."""
      msg = '\n'.join([head, cause])
      raise ValidationError(msg)
    return True
