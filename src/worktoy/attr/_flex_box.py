"""
FlexBox provides a dynamically typed version of AttriBox.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import AttriBox
from ..waitaminute import TypeException, CascadeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class FlexBox(AttriBox):
  """
  FlexBox provides a dynamically typed version of AttriBox.
  """

  def __instance_set__(self, val: Any, oldVal: Any = None, **kwargs) -> None:
    """
    Strongly typed setter requiring the new value to be a strict instance
    of the wrapped class.
    """
    try:
      AttriBox.__instance_set__(self, val, oldVal, **kwargs)
    except TypeException as typeException:
      cls = self.getWrappedClass()
      if typeException.varName == self.__field_name__:
        if typeException.actualObject == val:
          cls = self.getWrappedClass()
          exp = typeException.expectedType
          if cls in exp:
            try:
              value = cls(val)
            except Exception as exception:
              try:
                value = cls(*val)
              except Exception as exception2:
                errors = [
                    typeException,
                    exception,
                    exception2
                ]
                raise CascadeException(*errors)
            else:
              self.__instance_set__(value, oldVal, _recursion=True)
          else:
            print(typeException.expectedType, cls)
      else:
        raise typeException

    else:
      return
