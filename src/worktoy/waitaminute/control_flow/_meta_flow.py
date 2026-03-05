"""
MetaFlow provides the metaclass for the control flow exception classes. It
prevents these classes from having any sort of attributes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import VariableNotNone
from . import ControlSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias, Optional, Self, Union, Callable

  Bases: TypeAlias = tuple[Type[Any], ...]
  Space: TypeAlias = Union[ControlSpace, dict[str, Any]]
  STR: TypeAlias = Callable[[Self], str]


class MetaFlow(type):
  """
  MetaFlow provides the metaclass for the control flow exception classes. It
  prevents these classes from having any sort of attributes.
  """

  __is_root__: bool
  __root_cls__ = None

  @classmethod
  def getRootClass(mcls) -> Optional[Self]:
    return mcls.__root_cls__

  @classmethod
  def _registerRoot(mcls, cls: Self) -> None:
    if mcls.__root_cls__ is not None:
      raise VariableNotNone('__root_cls__', mcls.__root_cls__)
    mcls.__root_cls__ = cls

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    bases = (*[b for b in bases if b.__name__ != '_InitSub'],)
    space = ControlSpace(mcls, name, bases, **kwargs)
    strFunc = mcls._strFactory()
    dict.__setitem__(space, '__str__', strFunc)
    dict.__setitem__(space, '__repr__', strFunc)
    _root = True if kwargs.get('_root', False) else False
    dict.__setitem__(space, '__is_root__', _root)
    return space

  def __new__(mcls, name: str, bases: Bases, space: Space, **kw) -> Self:
    cls = type.__new__(mcls, name, bases, space)
    if cls.__is_root__:
      mcls._registerRoot(cls)
    return cls

  def __str__(cls, ) -> str:
    root = cls.getRootClass()
    if cls is root:
      infoSpec = '<%s: [Root]>'
      return infoSpec % cls.__name__
    infoSpec = '<%s: %s>'
    return infoSpec % (root.__name__, cls.__name__)

  __repr__ = __str__

  @staticmethod
  def _strFactory() -> STR:
    """
    Factory method generating a '__str__' method that shows for the
    instance the same as for the class.
    """

    def __str__(self, ) -> str:
      cls = type(self)
      return str(cls)

    return __str__
