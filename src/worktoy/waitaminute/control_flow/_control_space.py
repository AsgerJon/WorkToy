"""
ControlSpace provides the namespace object for the control flow
exceptions.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import maybe
from . import ControlClassError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias

  from . import MetaFlow

  Bases: TypeAlias = tuple[type, ...]
  Meta: TypeAlias = Type[MetaFlow]


class ControlSpace(dict):
  """
  ControlSpace provides the namespace object for the control flow
  exceptions.
  """

  __white_list__ = (
    '__firstlineno__',
    '__str__',
    '__repr__',
    '__namespace__',
    '__static_attributes__',
    )

  __is_root__ = None
  __metaclass__: Meta = None
  __base_classes__ = None
  __class_name__ = None

  @classmethod
  def _getWhiteList(cls, ) -> tuple[str, ...]:
    return maybe(cls.__white_list__, ())

  def __init__(self, mcls: Meta, name: str, bases: Bases, **kw) -> None:
    dict.__init__(self, )
    self.__metaclass__ = mcls
    self.__base_classes__ = bases
    self.__class_name__ = name
    self.__is_root__ = True if kw.get('_root', False) else False
    self['__namespace__'] = self

  def __setitem__(self, key: str, value: Any) -> None:
    if key in self._getWhiteList():
      return dict.__setitem__(self, key, value)
    if not maybe(self.__is_root__, False):
      try:
        existing = getattr(Exception, key)
      except AttributeError:
        raise ControlClassError(self, key)
      else:
        if callable(existing):
          raise ControlClassError(self, key)
    return dict.__setitem__(self, key, value)
