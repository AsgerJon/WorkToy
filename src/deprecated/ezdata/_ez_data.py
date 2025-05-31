"""EZData leverages the 'worktoy' library to provide a dataclass."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..mcls import FunctionType, AbstractMetaclass
from . import EZMeta
from ..waitaminute import TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self as Scope
  from typing import Any

Func = type('_', (type,), dict(__instancecheck__=callable))('_', (), {})


class EZData(AbstractMetaclass, metaclass=AbstractMetaclass):
  """EZData is a dataclass that provides a simple way to define data
  structures with validation and serialization capabilities. """

  @classmethod
  def __class_call__(mcls, name: str, *bases, **kwargs) -> Scope:
    """
    When calling EZData itself, the parent metaclass __call__ defers to
    this method.
    """

    baseClasses = []
    for base in bases:
      if isinstance(base, type):
        baseClasses.append(base)
        continue
      raise TypeException('base', base, type)
    space = mcls.__prepare__(name, (*baseClasses,), )
    slotNames = (k for k, v in kwargs.items())
    space['__slots__'] = (*slotNames,)
    space['__bases__'] = (*baseClasses,)
    slotTypes = {}
    slotValues = {}
    for k, v in kwargs.items():
      if isinstance(v, type):
        slotTypes[k] = v
        slotValues[k] = v()
      else:
        slotTypes[k] = type(v)
        slotValues[k] = v
    space['__slot_types__'] = slotTypes
    space['__slot_values__'] = slotValues
    # space['__str__'] =
    cls = mcls.__new__(mcls, name, (*baseClasses,), space)
    setattr(cls, '__str__', mcls.__str_factory__(cls))
    return cls

  def __str__(cls, ) -> str:
    """
    Returns a string representation fo the EZData class.
    """
    infoSpec = """%s: EZData%s(%s)"""
    bases = getattr(cls, '__bases__', )
    if bases:
      baseStr = '[%s]' % ', '.join(base.__name__ for base in bases)
    else:
      baseStr = ''
    clsName = type(cls).__name__
    typs = getattr(cls, '__slot_types__', )
    anns = ', '.join(['%s: %s' % (k, type(v).__name__) for k, v in typs])
    return infoSpec % (clsName, baseStr, anns)

  @staticmethod
  def __method_factory__(name: str, returnType: type) -> Func:
    """
    Returns a stub function that can be used as a placeholder for methods
    in the EZData class.
    """

    def func(self, *args, **kwargs) -> Any:
      """
      A stub function that can be used as a placeholder for methods in the
      EZData class.
      """

    setattr(func, '__name__', name)
    setattr(func, '__qualname__', name)
    #  Check if from __future__ import annotations is used
    NSpace = type(AbstractMetaclass.__prepare__.__annotations__['return'])
    if isinstance(NSpace, str):  # if True, then annotations are strings
      setattr(func, '__annotations__', {'return': returnType.__name__})
    else:
      setattr(func, '__annotations__', {'return': returnType})

  @staticmethod
  def __str_factory__(cls: type, ) -> Func:
    """
    Returns a string representation of the EZData class.
    """

    def __str__(self, ) -> str:
      """
      Returns a string representation of the EZData instance.
      """
      spec = str(cls)
      slotNames = getattr(cls, '__slots__', )
      slotTypes = getattr(cls, '__slot_types__', )
      for key, type_ in slotTypes:
        target = '%s: %s' % (key, type_)
        valSpec = '%s=%s' % (key, str(getattr(self, key, )))
        spec = spec.replace(target, valSpec, 1)
      return spec

    return __str__
