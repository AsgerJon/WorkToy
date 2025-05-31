"""
HistMetaclass provides a copy of AbstractMetaclass and BaseMeta with
HistDict providing the namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg, monoSpace
from worktoy.waitaminute import MissingVariable, HookException
from worktoy.waitaminute import QuestionableSyntax
from worktoy.mcls import Base, Types, Spaces, AbstractMetaclass
from worktoy.mcls import AbstractNamespace as ASpace
from worktoy.mcls.hooks import AbstractHook

from . import HistNameSpace as HSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never

  Bases: TypeAlias = tuple[type, ...]


class HistMetaclass(AbstractMetaclass):
  """
  HistMetaclass provides a copy of AbstractMetaclass and BaseMeta with
  HistDict providing the namespace.
  """

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> HSpace:
    """
    Prepares the namespace for the class being created.

    Args:
      name: str
        The name of the class.
      bases: Bases
        The base classes of the class.
      kwargs: dict
        Additional keyword arguments.

    Returns:
      HSpace: A HistNameSpace instance.
    """
    if TYPE_CHECKING:
      assert isinstance(mcls, AbstractMetaclass)
    return HSpace(mcls, name, bases, **kwargs)
