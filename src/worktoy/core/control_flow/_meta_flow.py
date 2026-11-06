"""
MetaFlow is the metaclass for the control-flow exception classes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...waitaminute import VariableNotNone
from .. import MetaType
from . import ControlSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Type, TypeAlias, Optional, Self, Union, Callable

  Bases: TypeAlias = tuple[Type[Any], ...]
  Space: TypeAlias = Union[ControlSpace, dict[str, Any]]
  STR: TypeAlias = Callable[[Self], str]


class MetaFlow(MetaType, metaclass=MetaType):
  """
  Some exceptions steer a protocol instead of reporting a failure, as
  'StopIteration' tells a loop to stop. worktoy needs such signals,
  'SkipSet' among them, and a project may add its own. A signal is
  caught by its type, so the family needs one root to catch them all, a
  text that names the signal whatever it was raised with, and class
  bodies limited to what a signal can sensibly hold.

  Implementation
  --------------

  '__prepare__' returns a 'ControlSpace', which refuses every name a
  signal may not define, already holding a '__str__' and '__repr__' that
  give the text of the class, and the flag '__is_root__' read from the
  class keyword '_root'. '__new__' builds the signal through 'MetaType'
  and records the one root, refusing a second with 'VariableNotNone'.
  The text of a signal class reads '<ControlFlow: SkipSet>', and the root
  reads '<ControlFlow: [Root]>'.

  Attributes
  ----------

  __root_cls__ : type or None
    The root signal, 'ControlFlow', once created.
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
    space = ControlSpace(mcls, name, bases, **kwargs)
    strFunc = mcls._strFactory()
    dict.__setitem__(space, '__str__', strFunc)
    dict.__setitem__(space, '__repr__', strFunc)
    _root = True if kwargs.get('_root', False) else False
    dict.__setitem__(space, '__is_root__', _root)
    return space

  def __new__(mcls, name: str, bases: Bases, space: Space, **kw) -> Self:
    cls = super().__new__(mcls, name, bases, space, **kw)
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

    def __str__(self, ) -> str:
      cls = type(self)
      return str(cls)

    return __str__
